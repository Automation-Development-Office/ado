"""Security real-leaks check (scored) for Ansible task and handler files."""
# flake8: noqa: E501, E203

from __future__ import annotations

import argparse
import json
import re
import sys

from dataclasses import asdict, dataclass, field
from pathlib import Path


PENALTY_CONFIRMED_LEAK = 25
PENALTY_HIGH_RISK_PATTERN = 10
PENALTY_TOKEN_URI_DEBUG_WARNING = 5

PASS_MIN_SCORE = 98
WARN_MIN_SCORE = 90

DEFAULT_CONFIG_PATH = Path(__file__).resolve().parent / "security_checks_config.yaml"

SECRET_VAR_RE = re.compile(
    r"(password|passwd|client_secret|clientSecret|bind_password|"
    r"pull_secret|private_key|\bsecret\b|(?<![_\w])token(?![_\w]))",
)
DEBUG_LINE_RE = re.compile(r"^\s*(debug:|ansible\.builtin\.debug:)")
NO_LOG_RE = re.compile(r"^\s*no_log:\s*true\s*$")
TASK_START_RE = re.compile(r"^\s*-\s+name:")
MSG_SECRET_RE = re.compile(r"msg:.*" + SECRET_VAR_RE.pattern)

HIGH_RISK_PHRASES = (
    "Print SA tokens to screen",
    'Authorization: "Bearer',
    "sasl_passwd:",
    "htpasswd",
    "client_secret",
    "access_token",
)

URI_TOKEN_RE = re.compile(
    r"(uri:|ansible\.builtin\.uri:|protocol/openid-connect/token|access_token)",
)
DEBUG_ANY_RE = re.compile(r"(debug:|ansible\.builtin\.debug:)")

TASK_GLOB_PATTERNS = (
    "**/tasks/*.yml",
    "**/tasks/*.yaml",
    "**/handlers/*.yml",
    "**/handlers/*.yaml",
)


DEFAULT_SKIP_HIGH_RISK_LINE_PATTERNS = (
    r"^\s*#",
    r"^\s*-\s+(when|failed_when):",
    r"\bis not defined\b",
    r"\bis defined\b",
    r"fail_msg:",
)


@dataclass
class PenaltyCaps:
    """Maximum score deduction allowed per category."""

    confirmed: int | None = None
    high_risk: int | None = 40
    warnings: int | None = 25


DEFAULT_PENALTY_CAPS = PenaltyCaps()


@dataclass
class SecurityScanConfig:
    """Loaded configuration for security checks."""

    penalty_caps: PenaltyCaps = field(default_factory=PenaltyCaps)
    score_high_risk_by_file_phrase: bool = True
    skip_high_risk_line_patterns: list[re.Pattern[str]] = field(default_factory=list)
    config_path: str | None = None


@dataclass
class ConfirmedFinding:
    file: str
    line: int


@dataclass
class HighRiskFinding:
    file: str
    line: int
    phrase: str
    text: str


@dataclass
class WarningFinding:
    file: str


@dataclass
class SecurityReport:
    root: str
    task_files_scanned: int
    confirmed_count: int
    highrisk_count: int
    warning_count: int
    score: int
    result: str
    confirmed_penalty: int = 0
    highrisk_penalty: int = 0
    warning_penalty: int = 0
    highrisk_penalty_cap: int | None = DEFAULT_PENALTY_CAPS.high_risk
    warning_penalty_cap: int | None = DEFAULT_PENALTY_CAPS.warnings
    pass_min_score: int = PASS_MIN_SCORE
    warn_min_score: int = WARN_MIN_SCORE
    confirmed_findings: list[ConfirmedFinding] = field(default_factory=list)
    highrisk_findings: list[HighRiskFinding] = field(default_factory=list)
    warning_findings: list[WarningFinding] = field(default_factory=list)


def parse_args() -> argparse.Namespace:
    """Parse command-line options."""
    parser = argparse.ArgumentParser(
        description="Run scored security checks on Ansible task/handler files.",
    )
    parser.add_argument(
        "root",
        nargs="?",
        default=".",
        help="Repository root to scan (default: current directory)",
    )
    parser.add_argument(
        "--config",
        metavar="PATH",
        default=str(DEFAULT_CONFIG_PATH),
        help=(
            "Security check config file (YAML or JSON). "
            f"Default: {DEFAULT_CONFIG_PATH.name} beside this script."
        ),
    )
    parser.add_argument(
        "--json-report",
        metavar="PATH",
        help="Write machine-readable JSON results to PATH",
    )
    parser.add_argument(
        "--summary-markdown",
        metavar="PATH",
        help="Write a GitHub Actions job summary markdown file to PATH",
    )
    return parser.parse_args()


def find_task_files(root: Path) -> list[Path]:
    """Return sorted task and handler YAML files under root."""
    files: set[Path] = set()
    for pattern in TASK_GLOB_PATTERNS:
        for path in root.glob(pattern):
            if path.is_file() and ".git" not in path.parts:
                files.add(path)
    return sorted(files)


def _compile_regex_patterns(patterns: list[str]) -> list[re.Pattern[str]]:
    """Compile regex patterns, ignoring invalid entries."""
    compiled: list[re.Pattern[str]] = []
    for pattern in patterns:
        try:
            compiled.append(re.compile(pattern, re.IGNORECASE))
        except re.error:
            print(f"Warning: ignoring invalid skip regex: {pattern}", file=sys.stderr)
    return compiled


def _penalty_caps_from_mapping(mapping: dict | None) -> PenaltyCaps:
    """Build PenaltyCaps from a config mapping."""
    if not mapping:
        return PenaltyCaps()

    def _cap_value(key: str, default: int | None) -> int | None:
        if key not in mapping:
            return default
        value = mapping[key]
        if value is None:
            return None
        return int(value)

    return PenaltyCaps(
        confirmed=_cap_value("confirmed", None),
        high_risk=_cap_value("high_risk", DEFAULT_PENALTY_CAPS.high_risk),
        warnings=_cap_value("warnings", DEFAULT_PENALTY_CAPS.warnings),
    )


def default_config() -> SecurityScanConfig:
    """Return built-in configuration when no config file is present."""
    return SecurityScanConfig(
        penalty_caps=DEFAULT_PENALTY_CAPS,
        skip_high_risk_line_patterns=_compile_regex_patterns(
            list(DEFAULT_SKIP_HIGH_RISK_LINE_PATTERNS),
        ),
    )


def load_config(config_path: Path) -> SecurityScanConfig:
    """Load security check configuration from YAML or JSON."""
    if not config_path.is_file():
        return default_config()

    raw_text = config_path.read_text(encoding="utf-8")
    if config_path.suffix.lower() == ".json":
        data = json.loads(raw_text)
    else:
        try:
            import yaml
        except ImportError as exc:
            raise SystemExit(
                "PyYAML is required to load YAML config files. Install with: pip install pyyaml",
            ) from exc
        data = yaml.safe_load(raw_text) or {}

    patterns = data.get("skip_high_risk_line_patterns") or DEFAULT_SKIP_HIGH_RISK_LINE_PATTERNS

    return SecurityScanConfig(
        penalty_caps=_penalty_caps_from_mapping(data.get("penalty_caps")),
        score_high_risk_by_file_phrase=bool(
            data.get("score_high_risk_by_file_phrase", True),
        ),
        skip_high_risk_line_patterns=_compile_regex_patterns(
            [str(item) for item in patterns],
        ),
        config_path=str(config_path),
    )


def task_has_no_log(lines: list[str], index: int, forward_window: int = 25) -> bool:
    """Return True when the surrounding Ansible task sets no_log: true."""
    for line_index in range(index, -1, -1):
        if TASK_START_RE.match(lines[line_index]) and line_index != index:
            break
        if NO_LOG_RE.match(lines[line_index]):
            return True

    for line_index in range(index + 1, min(len(lines), index + forward_window)):
        if NO_LOG_RE.match(lines[line_index]):
            return True

    return False


def is_skipped_high_risk_line(line: str, config: SecurityScanConfig) -> bool:
    """Return True when a line matches configured high-risk skip patterns."""
    return any(pattern.search(line) for pattern in config.skip_high_risk_line_patterns)


def suggest_no_log(file_path: Path, line: int, why: str) -> None:
    """Print remediation guidance for missing no_log on sensitive debug output."""
    print("     Suggestion:")
    print("       - Add: no_log: true")
    print(
        "       - (Optional) Gate debug behind a flag, e.g. when: <role>_debug | default(false)",
    )
    print(f"     Why: {why}")
    print("     Fix hint:")
    print(f"       edit {file_path} around line {line}")


def suggest_remove_debug(file_path: Path, line: int, why: str) -> None:
    """Print remediation guidance for debug tasks that expose secrets."""
    print("     Suggestion:")
    print("       - Remove the debug OR keep it but add: no_log: true")
    print("       - Prefer writing tokens to a Kubernetes Secret instead of printing")
    print(f"     Why: {why}")
    print("     Fix hint:")
    print(f"       edit {file_path} around line {line}")


def suggest_uri_no_log(file_path: Path, line: int, why: str) -> None:
    """Print remediation guidance for URI/token tasks that may leak responses."""
    print("     Suggestion:")
    print("       - Ensure the uri task has: no_log: true")
    print("       - Avoid debugging the registered response from token endpoints")
    print(f"     Why: {why}")
    print("     Fix hint:")
    print(f"       edit {file_path} around line {line}")


def high_risk_suggestion(file_path: Path, line: int, phrase: str) -> None:
    """Print phrase-specific remediation guidance."""
    suggestions = {
        "Print SA tokens to screen": (
            suggest_remove_debug,
            "ServiceAccount tokens should never be printed to logs.",
        ),
        "sasl_passwd:": (
            suggest_no_log,
            "SASL password lines include credentials; protect from log output and diff.",
        ),
        'Authorization: "Bearer': (
            suggest_no_log,
            "Bearer tokens in headers must not be logged or registered+debugged.",
        ),
        "htpasswd": (
            suggest_no_log,
            "htpasswd generation often touches raw passwords; keep tasks quiet.",
        ),
        "client_secret": (
            suggest_uri_no_log,
            "OIDC/LDAP token flows should not log request/response bodies.",
        ),
        "access_token": (
            suggest_uri_no_log,
            "OIDC/LDAP token flows should not log request/response bodies.",
        ),
    }
    suggest_fn, why = suggestions.get(phrase, (suggest_no_log, "Likely sensitive content."))
    suggest_fn(file_path, line, why)


def collect_confirmed_leaks(files: list[Path]) -> list[ConfirmedFinding]:
    """Collect debug tasks that may print sensitive values without no_log."""
    findings: list[ConfirmedFinding] = []

    for file_path in files:
        lines = file_path.read_text(encoding="utf-8", errors="replace").splitlines()
        for index, line in enumerate(lines):
            if not DEBUG_LINE_RE.match(line):
                continue

            line_number = index + 1
            snippet = lines[index : index + 25]
            has_secret_msg = any(MSG_SECRET_RE.search(snippet_line) for snippet_line in snippet)

            if has_secret_msg and not task_has_no_log(lines, index):
                findings.append(
                    ConfirmedFinding(file=str(file_path), line=line_number),
                )

    return findings


def collect_high_risk_patterns(
    files: list[Path],
    config: SecurityScanConfig,
) -> list[HighRiskFinding]:
    """Collect known high-risk phrases in task files."""
    findings: list[HighRiskFinding] = []

    for file_path in files:
        lines = file_path.read_text(encoding="utf-8", errors="replace").splitlines()
        for phrase in HIGH_RISK_PHRASES:
            for index, line in enumerate(lines):
                if phrase not in line:
                    continue
                if is_skipped_high_risk_line(line, config):
                    continue
                if task_has_no_log(lines, index):
                    continue
                findings.append(
                    HighRiskFinding(
                        file=str(file_path),
                        line=index + 1,
                        phrase=phrase,
                        text=line,
                    ),
                )

    return findings


def collect_token_uri_debug_warnings(files: list[Path]) -> list[WarningFinding]:
    """Collect files where token/URI usage and debug tasks both appear."""
    findings: list[WarningFinding] = []

    for file_path in files:
        content = file_path.read_text(encoding="utf-8", errors="replace")
        if URI_TOKEN_RE.search(content) and DEBUG_ANY_RE.search(content):
            findings.append(WarningFinding(file=str(file_path)))

    return findings


def _category_penalty(hit_count: int, per_hit: int, cap: int | None) -> int:
    """Apply per-hit penalty with an optional category cap."""
    raw_penalty = hit_count * per_hit
    if cap is None:
        return raw_penalty
    return min(raw_penalty, cap)


def highrisk_score_count(
    findings: list[HighRiskFinding],
    config: SecurityScanConfig,
) -> int:
    """Return the high-risk hit count used for scoring."""
    if config.score_high_risk_by_file_phrase:
        return len({(finding.file, finding.phrase) for finding in findings})
    return len(findings)


def score_report(
    confirmed_count: int,
    highrisk_count: int,
    warning_count: int,
    penalty_caps: PenaltyCaps,
) -> tuple[int, str, int, int, int, int]:
    """Return score, result, fail flag, and per-category penalties applied."""
    fail = 1 if confirmed_count > 0 else 0

    confirmed_penalty = _category_penalty(
        confirmed_count,
        PENALTY_CONFIRMED_LEAK,
        penalty_caps.confirmed,
    )
    highrisk_penalty = _category_penalty(
        highrisk_count,
        PENALTY_HIGH_RISK_PATTERN,
        penalty_caps.high_risk,
    )
    warning_penalty = _category_penalty(
        warning_count,
        PENALTY_TOKEN_URI_DEBUG_WARNING,
        penalty_caps.warnings,
    )

    score = 100 - confirmed_penalty - highrisk_penalty - warning_penalty
    score = max(score, 0)

    if fail == 1:
        result = "FAIL"
    elif score >= PASS_MIN_SCORE:
        result = "PASS"
    else:
        result = "WARN"

    return score, result, fail, confirmed_penalty, highrisk_penalty, warning_penalty


def run_checks(root: Path, config: SecurityScanConfig) -> SecurityReport:
    """Scan task files and return a structured security report."""
    task_files = find_task_files(root)
    confirmed_findings = collect_confirmed_leaks(task_files)
    highrisk_findings = collect_high_risk_patterns(task_files, config)
    warning_findings = collect_token_uri_debug_warnings(task_files)

    scored_highrisk_count = highrisk_score_count(highrisk_findings, config)

    (
        score,
        result,
        _fail,
        confirmed_penalty,
        highrisk_penalty,
        warning_penalty,
    ) = score_report(
        len(confirmed_findings),
        scored_highrisk_count,
        len(warning_findings),
        config.penalty_caps,
    )

    return SecurityReport(
        root=str(root),
        task_files_scanned=len(task_files),
        confirmed_count=len(confirmed_findings),
        highrisk_count=len(highrisk_findings),
        warning_count=len(warning_findings),
        score=score,
        result=result,
        confirmed_penalty=confirmed_penalty,
        highrisk_penalty=highrisk_penalty,
        warning_penalty=warning_penalty,
        highrisk_penalty_cap=config.penalty_caps.high_risk,
        warning_penalty_cap=config.penalty_caps.warnings,
        confirmed_findings=confirmed_findings,
        highrisk_findings=highrisk_findings,
        warning_findings=warning_findings,
    )


def print_confirmed_leaks(findings: list[ConfirmedFinding]) -> None:
    """Print confirmed leak findings."""
    print("[1/3] Confirmed leaks: debug prints secret-ish variables without no_log")
    for finding in findings:
        file_path = Path(finding.file)
        print(f"❌ CONFIRMED: {file_path}:{finding.line}")
        suggest_no_log(
            file_path,
            finding.line,
            "Printing tokens/passwords in logs is a real leak risk.",
        )
        print()
    print(f"  confirmed issues: {len(findings)}")
    print()


def print_high_risk_patterns(findings: list[HighRiskFinding]) -> None:
    """Print high-risk pattern findings."""
    print("[2/3] High-risk patterns (inspect + usually add no_log on the sensitive task)")
    for finding in findings:
        file_path = Path(finding.file)
        print(f"⚠️  HIGH-RISK: {file_path}:{finding.line}  ({finding.phrase})")
        print(f"     Hit: {finding.text}")
        high_risk_suggestion(file_path, finding.line, finding.phrase)
        print()
    print(f"  high-risk hits: {len(findings)}")
    print()


def print_token_uri_debug_warnings(findings: list[WarningFinding]) -> None:
    """Print token/URI plus debug warnings."""
    print("[3/3] Token-call + debug warnings (verify no_log + avoid dumping register vars)")
    for finding in findings:
        print(f"⚠️  WARNING: {finding.file} has token/uri + debug in same file")
        print("     Suggestion:")
        print("       - Ensure uri token tasks have: no_log: true")
        print("       - Never debug the registered result of token responses")
        print()
    print(f"  warnings: {len(findings)}")
    print()


def print_report(report: SecurityReport) -> None:
    """Print the human-readable security report."""
    print("== Security real-leaks check (scored) ==")
    print(f"Root: {report.root}")
    print()

    if report.task_files_scanned == 0:
        print("No task files found.")
        return

    print_confirmed_leaks(report.confirmed_findings)
    print_high_risk_patterns(report.highrisk_findings)
    print_token_uri_debug_warnings(report.warning_findings)

    print("== Summary ==")
    print(f"Confirmed issues: {report.confirmed_count}")
    print(f"High-risk hits: {report.highrisk_count}")
    print(f"Token/URI warnings: {report.warning_count}")
    print(
        "Penalties applied: "
        f"confirmed={report.confirmed_penalty}, "
        f"high_risk={report.highrisk_penalty}, "
        f"warnings={report.warning_penalty}",
    )
    print(f"Score: {report.score}/100")

    if report.result == "PASS":
        print(f"Result: ✅ PASS (>= {PASS_MIN_SCORE})")
    elif report.result == "WARN":
        print(f"Result: ⚠️  WARN (< {PASS_MIN_SCORE}, no confirmed leaks)")
    else:
        print("Result: ❌ FAIL (confirmed leaks found)")


def render_github_summary(report: SecurityReport) -> str:
    """Render a markdown dashboard for GitHub Actions job summaries."""
    if report.task_files_scanned == 0:
        return "## Security Check Dashboard\n\nNo task files found.\n"

    result_icon = {
        "PASS": "✅",
        "WARN": "⚠️",
        "FAIL": "❌",
    }[report.result]

    bar_chart_values = f"{report.score}, {PASS_MIN_SCORE}, {WARN_MIN_SCORE}"
    mermaid_bar_line = "    bar [" + bar_chart_values + "]"

    lines = [
        "## Security Check Dashboard",
        "",
        f"**Result:** {result_icon} {report.result}",
        f"**Score:** {report.score}/100",
        f"**Scan root:** `{report.root}`",
        f"**Task files scanned:** {report.task_files_scanned}",
        "",
        "| Category | Count | Penalty applied | Cap |",
        "| --- | ---: | ---: | ---: |",
        f"| Confirmed leaks | {report.confirmed_count} | {report.confirmed_penalty} | — |",
        (
            f"| High-risk patterns | {report.highrisk_count} | "
            f"{report.highrisk_penalty} | {report.highrisk_penalty_cap or '—'} |"
        ),
        (
            f"| Token/URI + debug warnings | {report.warning_count} | "
            f"{report.warning_penalty} | {report.warning_penalty_cap or '—'} |"
        ),
        "",
        "### Findings by category",
        "",
        "```mermaid",
        "pie showData",
        "    title Findings by category",
        f'    "Confirmed leaks" : {report.confirmed_count}',
        f'    "High-risk patterns" : {report.highrisk_count}',
        f'    "Token/URI warnings" : {report.warning_count}',
        "```",
        "",
        "### Security score",
        "",
        "```mermaid",
        "xychart-beta",
        '    title "Security score vs thresholds"',
        '    x-axis ["Score", "Pass", "Warn"]',
        '    y-axis "Points" 0 --> 100',
        mermaid_bar_line,
        "```",
        "",
        "> Informational only — not enforced in the PR gate yet.",
    ]

    if report.confirmed_findings:
        lines.extend(["", "### Confirmed leaks", ""])
        for finding in report.confirmed_findings[:20]:
            lines.append(f"- `{finding.file}:{finding.line}`")
        if len(report.confirmed_findings) > 20:
            lines.append(f"- …and {len(report.confirmed_findings) - 20} more (see JSON artifact)")

    return "\n".join(lines) + "\n"


def write_json_report(report: SecurityReport, path: Path) -> None:
    """Write the structured report as JSON."""
    path.write_text(
        json.dumps(asdict(report), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def write_summary_markdown(report: SecurityReport, path: Path) -> None:
    """Write the GitHub Actions summary markdown file."""
    path.write_text(render_github_summary(report), encoding="utf-8")


def exit_code_for_report(report: SecurityReport) -> int:
    """Return the process exit code for a completed report."""
    if report.task_files_scanned == 0:
        return 0
    if report.result in {"PASS", "WARN"}:
        return 0
    return 1


def main() -> int:
    """Run security checks and return the process exit code."""
    args = parse_args()
    root = Path(args.root).resolve()
    config = load_config(Path(args.config).resolve())
    report = run_checks(root, config)
    print_report(report)

    if args.json_report:
        write_json_report(report, Path(args.json_report))

    if args.summary_markdown:
        write_summary_markdown(report, Path(args.summary_markdown))

    return exit_code_for_report(report)


if __name__ == "__main__":
    sys.exit(main())
