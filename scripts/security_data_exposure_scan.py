"""Data exposure scan (org strings, IPs, hostnames, domains) with scoring."""
# flake8: noqa: E501, E203

from __future__ import annotations

import argparse
import json
import re
import sys

from dataclasses import asdict, dataclass, field
from fnmatch import fnmatch
from pathlib import Path


PENALTY_ORG_STRING = 30
PENALTY_PUBLIC_IP = 25
PENALTY_PRIVATE_IP = 1
PENALTY_INTERNAL_FQDN = 3

PASS_MIN_SCORE = 98

DEFAULT_CONFIG_PATH = Path(__file__).resolve().parent / "data_exposure_scan_config.yaml"

ORG_RE = re.compile(
    r"(FBI|Federal Bureau of Investigation|Federal Bureau of Investigations)",
)
IPV4_RE = re.compile(r"(?:[0-9]{1,3}\.){3}[0-9]{1,3}")
FQDN_RE = re.compile(
    r"([a-zA-Z0-9-]+\.)+(lab|local|internal|corp|com|gov|net|org)\b",
)
PRIVATE_IP_RE = re.compile(
    r"^(?:10\.|192\.168\.|172\.(?:1[6-9]|2[0-9]|3[0-1])\.|127\.)",
)

DEFAULT_SKIP_DIRECTORIES = {".git"}


@dataclass
class PenaltyCaps:
    """Maximum score deduction allowed per category."""

    org: int | None = None
    public_ip: int | None = None
    private_ip: int | None = 10
    fqdn: int | None = 30


DEFAULT_PENALTY_CAPS = PenaltyCaps()


@dataclass
class CategorySkipRules:
    """Skip rules for one finding category."""

    value_contains: list[str] = field(default_factory=list)
    value_regex: list[re.Pattern[str]] = field(default_factory=list)
    line_contains: list[str] = field(default_factory=list)
    file_patterns: list[str] = field(default_factory=list)


@dataclass
class ExposureScanConfig:
    """Loaded skip-list configuration for the exposure scan."""

    skip_directories: set[str] = field(default_factory=lambda: set(DEFAULT_SKIP_DIRECTORIES))
    skip_files: list[str] = field(default_factory=list)
    skip_line_contains: list[str] = field(default_factory=list)
    penalty_caps: PenaltyCaps = field(default_factory=PenaltyCaps)
    categories: dict[str, CategorySkipRules] = field(default_factory=dict)
    config_path: str | None = None


@dataclass
class ExposureFinding:
    file: str
    line: int
    text: str
    category: str
    matched_value: str = ""


@dataclass
class ExposureReport:
    root: str
    files_scanned: int
    org_hits: int
    private_ip_hits: int
    public_ip_hits: int
    fqdn_hits: int
    skipped_hits: int
    score: int
    result: str
    org_penalty: int = 0
    private_ip_penalty: int = 0
    public_ip_penalty: int = 0
    fqdn_penalty: int = 0
    private_ip_penalty_cap: int | None = DEFAULT_PENALTY_CAPS.private_ip
    fqdn_penalty_cap: int | None = DEFAULT_PENALTY_CAPS.fqdn
    config_path: str | None = None
    pass_min_score: int = PASS_MIN_SCORE
    org_findings: list[ExposureFinding] = field(default_factory=list)
    private_ip_findings: list[ExposureFinding] = field(default_factory=list)
    public_ip_findings: list[ExposureFinding] = field(default_factory=list)
    fqdn_findings: list[ExposureFinding] = field(default_factory=list)


def parse_args() -> argparse.Namespace:
    """Parse command-line options."""
    parser = argparse.ArgumentParser(
        description=(
            "Scan repository content for org-specific strings, IP addresses, " "and FQDN patterns."
        ),
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
            "Skip-list config file (YAML or JSON). "
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
        org=_cap_value("org", None),
        public_ip=_cap_value("public_ip", None),
        private_ip=_cap_value("private_ip", DEFAULT_PENALTY_CAPS.private_ip),
        fqdn=_cap_value("fqdn", DEFAULT_PENALTY_CAPS.fqdn),
    )


def _category_rules_from_mapping(mapping: dict) -> CategorySkipRules:
    """Build CategorySkipRules from a config mapping."""
    return CategorySkipRules(
        value_contains=[str(item) for item in mapping.get("value_contains", [])],
        value_regex=_compile_regex_patterns(
            [str(item) for item in mapping.get("value_regex", [])],
        ),
        line_contains=[str(item) for item in mapping.get("line_contains", [])],
        file_patterns=[str(item) for item in mapping.get("file_patterns", [])],
    )


def default_config() -> ExposureScanConfig:
    """Return built-in skip rules used when no config file is present."""
    return ExposureScanConfig(
        categories={
            "fqdn": CategorySkipRules(
                value_contains=["example", ".example."],
                value_regex=_compile_regex_patterns(
                    [r"\.example(\.|$)", r"(^|\.)example\."],
                ),
            ),
            "org": CategorySkipRules(),
            "public_ip": CategorySkipRules(
                value_contains=[
                    "192.0.2.",
                    "198.51.100.",
                    "203.0.113.",
                    "1.1.1.1",
                    "8.8.8.8",
                ],
            ),
            "private_ip": CategorySkipRules(),
        },
        penalty_caps=DEFAULT_PENALTY_CAPS,
    )


def load_config(config_path: Path) -> ExposureScanConfig:
    """Load skip-list config from YAML or JSON."""
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
                "PyYAML is required to load YAML config files. " "Install with: pip install pyyaml",
            ) from exc
        data = yaml.safe_load(raw_text) or {}

    categories: dict[str, CategorySkipRules] = {}
    for category_name, category_data in (data.get("categories") or {}).items():
        if isinstance(category_data, dict):
            categories[str(category_name)] = _category_rules_from_mapping(category_data)

    skip_directories = set(data.get("skip_directories") or DEFAULT_SKIP_DIRECTORIES)
    skip_files = [str(item) for item in data.get("skip_files") or []]
    skip_line_contains = [str(item) for item in data.get("skip_line_contains") or []]
    penalty_caps = _penalty_caps_from_mapping(data.get("penalty_caps"))

    return ExposureScanConfig(
        skip_directories=skip_directories,
        skip_files=skip_files,
        skip_line_contains=skip_line_contains,
        penalty_caps=penalty_caps,
        categories=categories,
        config_path=str(config_path),
    )


def should_skip_finding(
    finding: ExposureFinding,
    config: ExposureScanConfig,
) -> bool:
    """Return True when a finding matches configured skip rules."""
    line_text = finding.text.casefold()

    if any(substring.casefold() in line_text for substring in config.skip_line_contains):
        return True

    rules = config.categories.get(finding.category)
    if rules is None:
        return False

    matched_value = finding.matched_value.casefold()

    if any(substring.casefold() in matched_value for substring in rules.value_contains):
        return True

    if any(pattern.search(finding.matched_value) for pattern in rules.value_regex):
        return True

    if any(substring.casefold() in line_text for substring in rules.line_contains):
        return True

    if rules.file_patterns and any(
        fnmatch(finding.file, pattern) for pattern in rules.file_patterns
    ):
        return True

    return False


def iter_scan_files(root: Path, config: ExposureScanConfig) -> list[Path]:
    """Return text files under root, honoring configured directory skips."""
    files: list[Path] = []

    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        if any(part in config.skip_directories for part in path.parts):
            continue
        relative_path = str(path.relative_to(root))
        if any(fnmatch(relative_path, pattern) for pattern in config.skip_files):
            continue
        if _looks_binary(path):
            continue
        files.append(path)

    return files


def _looks_binary(path: Path) -> bool:
    """Return True when a file appears to be binary."""
    try:
        with path.open("rb") as handle:
            chunk = handle.read(8192)
    except OSError:
        return True
    return b"\0" in chunk


def classify_ip(ip_address: str) -> str:
    """Classify an IPv4 address as private or public using shell heuristics."""
    if PRIVATE_IP_RE.match(ip_address):
        return "private_ip"
    return "public_ip"


def scan_file(
    path: Path,
    root: Path,
    config: ExposureScanConfig,
) -> tuple[list[ExposureFinding], int]:
    """Scan one file for org strings, IPs, and FQDN patterns."""
    findings: list[ExposureFinding] = []
    skipped = 0
    display_path = str(path.relative_to(root))

    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return findings, skipped

    for line_number, line in enumerate(lines, start=1):
        for org_match in ORG_RE.finditer(line):
            finding = ExposureFinding(
                file=display_path,
                line=line_number,
                text=line.rstrip(),
                category="org",
                matched_value=org_match.group(0),
            )
            if should_skip_finding(finding, config):
                skipped += 1
                continue
            findings.append(finding)

        for ip_match in IPV4_RE.finditer(line):
            ip_address = ip_match.group(0)
            finding = ExposureFinding(
                file=display_path,
                line=line_number,
                text=line.rstrip(),
                category=classify_ip(ip_address),
                matched_value=ip_address,
            )
            if should_skip_finding(finding, config):
                skipped += 1
                continue
            findings.append(finding)

        for fqdn_match in FQDN_RE.finditer(line):
            finding = ExposureFinding(
                file=display_path,
                line=line_number,
                text=line.rstrip(),
                category="fqdn",
                matched_value=fqdn_match.group(0),
            )
            if should_skip_finding(finding, config):
                skipped += 1
                continue
            findings.append(finding)

    return findings, skipped


def deduplicate_findings(findings: list[ExposureFinding]) -> list[ExposureFinding]:
    """Keep one finding per file, line, and category (grep line semantics)."""
    seen: set[tuple[str, int, str]] = set()
    unique: list[ExposureFinding] = []

    for finding in findings:
        key = (finding.file, finding.line, finding.category)
        if key in seen:
            continue
        seen.add(key)
        unique.append(finding)

    return unique


def _category_penalty(hit_count: int, per_hit: int, cap: int | None) -> int:
    """Apply per-hit penalty with an optional category cap."""
    raw_penalty = hit_count * per_hit
    if cap is None:
        return raw_penalty
    return min(raw_penalty, cap)


def score_report(
    org_hits: int,
    private_ip_hits: int,
    public_ip_hits: int,
    fqdn_hits: int,
    penalty_caps: PenaltyCaps,
) -> tuple[int, str, int, int, int, int, int]:
    """Return score, result, fail flag, and per-category penalties applied."""
    org_penalty = _category_penalty(org_hits, PENALTY_ORG_STRING, penalty_caps.org)
    private_ip_penalty = _category_penalty(
        private_ip_hits,
        PENALTY_PRIVATE_IP,
        penalty_caps.private_ip,
    )
    public_ip_penalty = _category_penalty(
        public_ip_hits,
        PENALTY_PUBLIC_IP,
        penalty_caps.public_ip,
    )
    fqdn_penalty = _category_penalty(fqdn_hits, PENALTY_INTERNAL_FQDN, penalty_caps.fqdn)

    score = 100 - org_penalty - private_ip_penalty - public_ip_penalty - fqdn_penalty
    score = max(score, 0)

    if org_hits > 0 or public_ip_hits > 0:
        return score, "FAIL", 1, org_penalty, private_ip_penalty, public_ip_penalty, fqdn_penalty
    if score >= PASS_MIN_SCORE:
        return score, "PASS", 0, org_penalty, private_ip_penalty, public_ip_penalty, fqdn_penalty
    return score, "WARN", 0, org_penalty, private_ip_penalty, public_ip_penalty, fqdn_penalty


def run_scan(root: Path, config: ExposureScanConfig) -> ExposureReport:
    """Scan files and return a structured exposure report."""
    files = iter_scan_files(root, config)
    all_findings: list[ExposureFinding] = []
    skipped_hits = 0

    for path in files:
        file_findings, file_skipped = scan_file(path, root, config)
        all_findings.extend(file_findings)
        skipped_hits += file_skipped

    all_findings = deduplicate_findings(all_findings)

    org_findings = [finding for finding in all_findings if finding.category == "org"]
    private_ip_findings = [finding for finding in all_findings if finding.category == "private_ip"]
    public_ip_findings = [finding for finding in all_findings if finding.category == "public_ip"]
    fqdn_findings = [finding for finding in all_findings if finding.category == "fqdn"]

    (
        score,
        result,
        _fail,
        org_penalty,
        private_ip_penalty,
        public_ip_penalty,
        fqdn_penalty,
    ) = score_report(
        len(org_findings),
        len(private_ip_findings),
        len(public_ip_findings),
        len(fqdn_findings),
        config.penalty_caps,
    )

    return ExposureReport(
        root=str(root),
        files_scanned=len(files),
        org_hits=len(org_findings),
        private_ip_hits=len(private_ip_findings),
        public_ip_hits=len(public_ip_findings),
        fqdn_hits=len(fqdn_findings),
        skipped_hits=skipped_hits,
        score=score,
        result=result,
        org_penalty=org_penalty,
        private_ip_penalty=private_ip_penalty,
        public_ip_penalty=public_ip_penalty,
        fqdn_penalty=fqdn_penalty,
        private_ip_penalty_cap=config.penalty_caps.private_ip,
        fqdn_penalty_cap=config.penalty_caps.fqdn,
        config_path=config.config_path,
        org_findings=org_findings,
        private_ip_findings=private_ip_findings,
        public_ip_findings=public_ip_findings,
        fqdn_findings=fqdn_findings,
    )


def print_findings(title: str, findings: list[ExposureFinding], suggestion: str) -> None:
    """Print a category section with grep-style hits."""
    print(title)
    if not findings:
        print("  (none found)")
        print()
        return

    for finding in findings:
        print(f"{finding.file}:{finding.line}:{finding.text}")
    print()
    print(f"  Suggestion: {suggestion}")
    print()


def print_report(report: ExposureReport) -> None:
    """Print the human-readable exposure report."""
    print("== Data exposure scan (org strings, IPs, hostnames, domains) ==")
    print(f"Root: {report.root}")
    if report.config_path:
        print(f"Config: {report.config_path}")
    print()

    print_findings(
        "[1/3] Organization terms...",
        report.org_findings,
        "remove/replace org-specific strings with neutral placeholders " "(e.g., <agency>, <org>).",
    )
    print_findings(
        "[2/3] IPv4 addresses...",
        report.private_ip_findings + report.public_ip_findings,
        (
            "Private IPs in docs/examples are usually OK. "
            "Public/routable IPs should be removed or moved to env vault/vars."
        ),
    )
    print_findings(
        "[3/3] FQDN/hostname patterns...",
        report.fqdn_findings,
        (
            "If hostnames are in README/molecule docs: OK (consider placeholders). "
            "If hostnames are hard-coded in tasks/defaults: move to env vars/vault "
            "(domain/app_domain/app_domain_alt)."
        ),
    )

    print("== Summary ==")
    print(f"Org hits: {report.org_hits}")
    print(f"Private IP hits: {report.private_ip_hits}")
    print(f"Public IP hits: {report.public_ip_hits}")
    print(f"FQDN hits: {report.fqdn_hits}")
    print(f"Skipped hits: {report.skipped_hits}")
    print(
        "Penalties applied: "
        f"org={report.org_penalty}, "
        f"public_ip={report.public_ip_penalty}, "
        f"private_ip={report.private_ip_penalty}, "
        f"fqdn={report.fqdn_penalty}",
    )
    print(f"Score: {report.score}/100")

    if report.result == "PASS":
        print("Result: ✅ PASS")
    elif report.result == "WARN":
        print("Result: ⚠️  WARN (score < 98, review suggestions)")
    else:
        print("Result: ❌ FAIL (org strings or public IPs found)")


def render_github_summary(report: ExposureReport) -> str:
    """Render a markdown dashboard for GitHub Actions job summaries."""
    result_icon = {
        "PASS": "✅",
        "WARN": "⚠️",
        "FAIL": "❌",
    }[report.result]

    bar_chart_values = f"{report.score}, {PASS_MIN_SCORE}"
    mermaid_bar_line = "    bar [" + bar_chart_values + "]"
    config_line = (
        f"**Config:** `{report.config_path}`"
        if report.config_path
        else "**Config:** built-in defaults"
    )

    lines = [
        "## Data Exposure Scan Dashboard",
        "",
        f"**Result:** {result_icon} {report.result}",
        f"**Score:** {report.score}/100",
        f"**Scan root:** `{report.root}`",
        config_line,
        f"**Files scanned:** {report.files_scanned}",
        f"**Skipped hits:** {report.skipped_hits}",
        "",
        "| Category | Count | Penalty applied | Cap |",
        "| --- | ---: | ---: | ---: |",
        f"| Organization terms | {report.org_hits} | {report.org_penalty} | — |",
        f"| Public IPv4 addresses | {report.public_ip_hits} | {report.public_ip_penalty} | — |",
        (
            f"| Private IPv4 addresses | {report.private_ip_hits} | "
            f"{report.private_ip_penalty} | {report.private_ip_penalty_cap or '—'} |"
        ),
        (
            f"| FQDN/hostname patterns | {report.fqdn_hits} | "
            f"{report.fqdn_penalty} | {report.fqdn_penalty_cap or '—'} |"
        ),
        "",
        "### Findings by category",
        "",
        "```mermaid",
        "pie showData",
        "    title Findings by category",
        f'    "Organization terms" : {report.org_hits}',
        f'    "Public IPv4" : {report.public_ip_hits}',
        f'    "Private IPv4" : {report.private_ip_hits}',
        f'    "FQDN patterns" : {report.fqdn_hits}',
        "```",
        "",
        "### Exposure score",
        "",
        "```mermaid",
        "xychart-beta",
        '    title "Exposure score vs pass threshold"',
        '    x-axis ["Score", "Pass"]',
        '    y-axis "Points" 0 --> 100',
        mermaid_bar_line,
        "```",
        "",
        "> Informational only — not enforced in the PR gate yet.",
    ]

    hard_fail_findings = report.org_findings + report.public_ip_findings
    if hard_fail_findings:
        lines.extend(["", "### Hard-fail findings", ""])
        for finding in hard_fail_findings[:20]:
            lines.append(f"- `{finding.file}:{finding.line}` ({finding.matched_value})")
        if len(hard_fail_findings) > 20:
            lines.append(f"- …and {len(hard_fail_findings) - 20} more (see JSON artifact)")

    return "\n".join(lines) + "\n"


def write_json_report(report: ExposureReport, path: Path) -> None:
    """Write the structured report as JSON."""
    path.write_text(
        json.dumps(asdict(report), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def write_summary_markdown(report: ExposureReport, path: Path) -> None:
    """Write the GitHub Actions summary markdown file."""
    path.write_text(render_github_summary(report), encoding="utf-8")


def exit_code_for_report(report: ExposureReport) -> int:
    """Return the process exit code for a completed report."""
    if report.result == "FAIL":
        return 1
    return 0


def main() -> int:
    """Run the data exposure scan and return the process exit code."""
    args = parse_args()
    root = Path(args.root).resolve()
    config = load_config(Path(args.config).resolve())
    report = run_scan(root, config)
    print_report(report)

    if args.json_report:
        write_json_report(report, Path(args.json_report))

    if args.summary_markdown:
        write_summary_markdown(report, Path(args.summary_markdown))

    return exit_code_for_report(report)


if __name__ == "__main__":
    sys.exit(main())
