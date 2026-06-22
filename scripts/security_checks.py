#!/usr/bin/env python3
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

SECRET_VAR_RE = re.compile(
    r"(password|passwd|token|client_secret|clientSecret|bind_password|"
    r"pull_secret|private_key|secret)",
)
DEBUG_LINE_RE = re.compile(r"^\s*(debug:|ansible\.builtin\.debug:)")
NO_LOG_RE = re.compile(r"^\s*no_log:\s*true\s*$")
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


def suggest_no_log(file_path: Path, line: int, why: str) -> None:
    """Print remediation guidance for missing no_log on sensitive debug output."""
    print("     Suggestion:")
    print("       - Add: no_log: true")
    print(
        "       - (Optional) Gate debug behind a flag, " "e.g. when: <role>_debug | default(false)",
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
            has_no_log = any(NO_LOG_RE.match(snippet_line) for snippet_line in snippet)
            has_secret_msg = any(MSG_SECRET_RE.search(snippet_line) for snippet_line in snippet)

            if has_secret_msg and not has_no_log:
                findings.append(
                    ConfirmedFinding(file=str(file_path), line=line_number),
                )

    return findings


def collect_high_risk_patterns(files: list[Path]) -> list[HighRiskFinding]:
    """Collect known high-risk phrases in task files."""
    findings: list[HighRiskFinding] = []

    for file_path in files:
        lines = file_path.read_text(encoding="utf-8", errors="replace").splitlines()
        for phrase in HIGH_RISK_PHRASES:
            for line_number, line in enumerate(lines, start=1):
                if phrase not in line:
                    continue
                findings.append(
                    HighRiskFinding(
                        file=str(file_path),
                        line=line_number,
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


def score_report(
    confirmed_count: int,
    highrisk_count: int,
    warning_count: int,
) -> tuple[int, str, int]:
    """Return score, result label, and fail flag for the collected counts."""
    score = 100
    fail = 0

    if confirmed_count > 0:
        score -= confirmed_count * PENALTY_CONFIRMED_LEAK
        fail = 1

    if highrisk_count > 0:
        score -= highrisk_count * PENALTY_HIGH_RISK_PATTERN

    if warning_count > 0:
        score -= warning_count * PENALTY_TOKEN_URI_DEBUG_WARNING

    score = max(score, 0)

    if score >= PASS_MIN_SCORE and fail == 0:
        result = "PASS"
    elif score >= WARN_MIN_SCORE and fail == 0:
        result = "WARN"
    else:
        result = "FAIL"

    return score, result, fail


def run_checks(root: Path) -> SecurityReport:
    """Scan task files and return a structured security report."""
    task_files = find_task_files(root)
    confirmed_findings = collect_confirmed_leaks(task_files)
    highrisk_findings = collect_high_risk_patterns(task_files)
    warning_findings = collect_token_uri_debug_warnings(task_files)

    score, result, _fail = score_report(
        len(confirmed_findings),
        len(highrisk_findings),
        len(warning_findings),
    )

    return SecurityReport(
        root=str(root),
        task_files_scanned=len(task_files),
        confirmed_count=len(confirmed_findings),
        highrisk_count=len(highrisk_findings),
        warning_count=len(warning_findings),
        score=score,
        result=result,
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
    print(f"Score: {report.score}/100")

    if report.result == "PASS":
        print(f"Result: ✅ PASS (>= {PASS_MIN_SCORE})")
    elif report.result == "WARN":
        print(f"Result: ⚠️  WARN (>= {WARN_MIN_SCORE}, < {PASS_MIN_SCORE})")
    else:
        print(f"Result: ❌ FAIL (< {WARN_MIN_SCORE} OR confirmed leaks found)")


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
        "| Category | Count | Penalty each |",
        "| --- | ---: | ---: |",
        f"| Confirmed leaks | {report.confirmed_count} | {PENALTY_CONFIRMED_LEAK} |",
        f"| High-risk patterns | {report.highrisk_count} | {PENALTY_HIGH_RISK_PATTERN} |",
        f"| Token/URI + debug warnings | {report.warning_count} | {PENALTY_TOKEN_URI_DEBUG_WARNING} |",
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
    report = run_checks(root)
    print_report(report)

    if args.json_report:
        write_json_report(report, Path(args.json_report))

    if args.summary_markdown:
        write_summary_markdown(report, Path(args.summary_markdown))

    return exit_code_for_report(report)


if __name__ == "__main__":
    sys.exit(main())
