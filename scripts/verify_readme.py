"""Verify role README.md format against a template heading layout."""

from __future__ import annotations

import argparse
import os
import re
import sys

from pathlib import Path


DEFAULT_TEMPLATE_DIR = Path("docs") / "templates"
DEFAULT_TEMPLATE_FILENAME = "role_readme_format_template.md"
DEFAULT_TEMPLATE_PATH = DEFAULT_TEMPLATE_DIR / DEFAULT_TEMPLATE_FILENAME
HEADING_PATTERN = r"^(#{1,6})\s+(.+?)\s*$"
HEADING_RE = re.compile(HEADING_PATTERN, re.MULTILINE)
VARIABLES_TABLE_HEADER_RE = re.compile(
    r"^\|[^\n]*Variable[^\n]*Description[^\n]*\|",
    re.MULTILINE | re.IGNORECASE,
)
VARIABLES_TABLE_SEPARATOR_RE = re.compile(
    r"^\|[-:\s|]+\|$",
    re.MULTILINE,
)
VARIABLES_TABLE_DATA_ROW_RE = re.compile(
    r"^\|[^\n`]*`[^`]+`[^\n]*\|",
    re.MULTILINE,
)
EXAMPLE_CODE_BLOCK_RE = re.compile(
    r"```(?:yaml|yml|ansible|bash)[\s\S]*?```",
    re.MULTILINE | re.IGNORECASE,
)


def parse_args() -> argparse.Namespace:
    """Parse command-line options for README verification."""
    parser = argparse.ArgumentParser(description="Verify role README format")
    parser.add_argument(
        "readme",
        nargs="?",
        help=(
            "Optional role README.md path to verify. "
            "If omitted, verify all roles/*/README.md files."
        ),
    )
    parser.add_argument(
        "--template",
        default=str(DEFAULT_TEMPLATE_PATH),
        help=(
            "Template README path, relative to repository root "
            "or absolute path. "
            f"Default: {DEFAULT_TEMPLATE_PATH}"
        ),
    )
    return parser.parse_args()


def find_repo_root(start: Path, template_relative_path: Path) -> Path:
    """Find repository root by locating the provided template README path."""
    current = start.resolve()
    for candidate in [current, *current.parents]:
        if (candidate / template_relative_path).is_file():
            return candidate
    tpl_path = template_relative_path
    tpl_msg = f"Could not locate template README at {tpl_path}"
    raise FileNotFoundError(f"{tpl_msg} from {start}")


def find_repo_root_from_context(start: Path) -> Path:
    """Find repository root from current context."""
    current = start.resolve()
    for candidate in [current, *current.parents]:
        has_roles_dir = (candidate / "roles").is_dir()
        has_galaxy_file = (candidate / "galaxy.yml").is_file()
        if has_roles_dir and has_galaxy_file:
            return candidate
    raise FileNotFoundError(f"Could not locate repository root from {start}")


def get_readme_files(root: Path) -> list[Path]:
    """Find role-level README.md files under roles/<role>/README.md."""
    roles_dir = root / "roles"
    readmes: list[Path] = []

    if not roles_dir.is_dir():
        return readmes

    for role_dir in sorted(p for p in roles_dir.iterdir() if p.is_dir()):
        candidate = role_dir / "README.md"
        if candidate.is_file():
            readmes.append(candidate)

    return readmes


def resolve_readme_files(
    repo_root: Path,
    readme_arg: str | None,
) -> list[Path]:
    """Return README paths to verify from an optional CLI path argument."""
    if readme_arg is None:
        return get_readme_files(repo_root)

    readme_path = Path(readme_arg)
    if not readme_path.is_absolute():
        readme_path = Path(os.getcwd()) / readme_path
    readme_path = readme_path.resolve()

    if not readme_path.is_file():
        raise FileNotFoundError(f"README not found: {readme_path}")

    return [readme_path]


def load_text(path: Path) -> str:
    """Read UTF-8 content from a text file."""
    return path.read_text(encoding="utf-8")


def format_issue(filepath: Path, line: int | None, message: str) -> str:
    """Format a verification issue with an optional source line number."""
    if line is not None:
        return f"{filepath}: Line {line}: {message}"
    return f"{filepath}: {message}"


def get_section_by_title_suffix(
    content: str,
    title_suffix: str,
) -> tuple[str, int] | None:
    """Return section body and 1-based heading line for a matching heading."""
    lines = content.splitlines(keepends=True)
    headings: list[tuple[int, int, str]] = []
    for line_index, line in enumerate(lines):
        match = HEADING_RE.match(line.rstrip("\n"))
        if match:
            headings.append(
                (line_index, len(match.group(1)), match.group(2).strip()),
            )

    suffix = title_suffix.lower()
    for heading_index, (line_index, level, title) in enumerate(headings):
        if suffix not in title.lower():
            continue
        start = line_index + 1
        end = len(lines)
        next_heading_index = heading_index + 1
        remaining_headings = headings[next_heading_index:]
        for next_heading in remaining_headings:
            next_line_index = next_heading[0]
            next_level = next_heading[1]
            if next_level <= level:
                end = next_line_index
                break
        return "".join(lines[start:end]), line_index + 1
    return None


def extract_heading_sequence(content: str) -> list[tuple[int, str, int]]:
    """Return heading tuples as (level, normalized_title, line_number)."""
    headings: list[tuple[int, str, int]] = []
    for match in HEADING_RE.finditer(content):
        level = len(match.group(1))
        title = re.sub(r"\s+", " ", match.group(2).strip())
        line_no = content[: match.start()].count("\n") + 1
        headings.append((level, title, line_no))
    return headings


def next_same_level_heading(
    headings: list[tuple[int, str, int]],
    start: int,
    level: int,
) -> tuple[int, tuple[int, str, int]] | None:
    """Return the index and next heading at the requested level, if any."""
    for index in range(start, len(headings)):
        if headings[index][0] == level:
            return index, headings[index]
    return None


def validate_headings_against_template(
    filepath: Path,
    content: str,
    template_headings: list[tuple[int, str]],
) -> list[str]:
    """Ensure README contains template section headings in the same order."""
    issues: list[str] = []
    headings = extract_heading_sequence(content)

    if not headings:
        issues.append(format_issue(filepath, 1, "Missing headings"))
        return issues

    # First heading is role-specific. Validate shape, not exact text.
    first_level, first_title, first_line = headings[0]
    role_pattern = r"^Role:\s+(`[^`]+`|[^\n`]+)$"
    if first_level != 1 or not re.match(role_pattern, first_title):
        err = "First heading should match '# Role: name' or '# Role: `name`'"
        issues.append(format_issue(filepath, first_line, err))

    # Match section/subsection structure from template, excluding H1 title.
    expected_sections = [h for h in template_headings if h[0] >= 2]
    position = 0
    last_matched_line = first_line
    eof_suggest_line: int | None = None
    for expected in expected_sections:
        expected_level, expected_title = expected[0], expected[1]
        found = False
        for i in range(position, len(headings)):
            level, title, line_no = headings[i]
            if (level, title) == (expected_level, expected_title):
                found = True
                position = i + 1
                last_matched_line = line_no
                eof_suggest_line = None
                break
        if not found:
            heading_str = "#" * expected_level
            substitute = next_same_level_heading(
                headings,
                position,
                expected_level,
            )
            if substitute is not None:
                substitute_index, heading = substitute
                _level, wrong_title, wrong_line = heading
                position = substitute_index + 1
                eof_suggest_line = None
                err = (
                    f"Missing heading: {heading_str} {expected_title} "
                    f"(found '{heading_str} {wrong_title}' instead)"
                )
                issues.append(format_issue(filepath, wrong_line, err))
                continue

            if eof_suggest_line is None:
                fallback_line = last_matched_line
                for level, _title, line_no in headings[position:]:
                    if level >= expected_level:
                        fallback_line = line_no
                        break
                else:
                    if headings:
                        fallback_line = headings[-1][2]
                    else:
                        fallback_line = last_matched_line
                eof_suggest_line = fallback_line

            err = f"Missing heading: {heading_str} {expected_title}"
            issues.append(format_issue(filepath, eof_suggest_line, err))
            eof_suggest_line += 1

    return issues


def validate_role_directory_name(filepath: Path) -> list[str]:
    """Ensure role directory names do not contain hyphens."""
    issues: list[str] = []
    if filepath.parent.parent.name != "roles":
        return issues

    role_name = filepath.parent.name
    if "-" in role_name:
        issues.append(
            format_issue(
                filepath,
                None,
                f"Role directory name '{role_name}' must not contain hyphens",
            ),
        )
    return issues


def validate_variables_table(filepath: Path, content: str) -> list[str]:
    """Ensure the Role Variables section contains a variables table."""
    issues: list[str] = []
    section = get_section_by_title_suffix(content, "Role Variables")
    if section is None:
        return issues

    section_body, section_line = section
    if not VARIABLES_TABLE_HEADER_RE.search(section_body):
        issues.append(
            format_issue(
                filepath,
                section_line,
                "Role Variables section must include a table header row with "
                "Variable and Description columns "
                "(for example, `| Variable | Description |`).",
            ),
        )
        return issues

    if not VARIABLES_TABLE_SEPARATOR_RE.search(section_body):
        issues.append(
            format_issue(
                filepath,
                section_line,
                "Role Variables table must include a separator row "
                "(for example, `|---------|-------------|`).",
            ),
        )

    if not VARIABLES_TABLE_DATA_ROW_RE.search(section_body):
        issues.append(
            format_issue(
                filepath,
                section_line,
                "Role Variables table must include at least one data row "
                "with a backtick-wrapped variable name.",
            ),
        )

    return issues


def validate_example_code_block(filepath: Path, content: str) -> list[str]:
    """Ensure the README includes an example fenced code block."""
    if EXAMPLE_CODE_BLOCK_RE.search(content):
        return []
    return [
        format_issue(
            filepath,
            None,
            "README must include an example fenced code block using "
            "```yaml, ```yml, ```ansible, or ```bash.",
        ),
    ]


def check_readme_format(
    filepath: Path,
    template_headings: list[tuple[int, str]],
) -> list[str]:
    """Verify README.md format and structure against the template."""
    content = load_text(filepath)
    issues: list[str] = []
    headings = extract_heading_sequence(content)

    # Verify file starts with a main heading.
    if not re.match(r"^#\s+", content):
        issues.append(
            format_issue(filepath, 1, "Missing main heading (# Title)"),
        )

    # Verify at least one subheading exists.
    if not re.search(r"^##\s+", content, re.MULTILINE):
        line = headings[0][2] if headings else 1
        issues.append(
            format_issue(filepath, line, "Missing subheadings (## Section)"),
        )

    template_issues = validate_headings_against_template(
        filepath,
        content,
        template_headings,
    )
    issues.extend(template_issues)
    issues.extend(validate_role_directory_name(filepath))
    issues.extend(validate_variables_table(filepath, content))
    issues.extend(validate_example_code_block(filepath, content))

    # Check for consistent line endings.
    lines = content.splitlines(keepends=True)
    crlf_lines: list[int] = []
    lf_only_lines: list[int] = []
    for line_no, line in enumerate(lines, 1):
        if line.endswith("\r\n"):
            crlf_lines.append(line_no)
        elif line.endswith("\n"):
            lf_only_lines.append(line_no)
    if crlf_lines and lf_only_lines:
        first_mixed_line = min(crlf_lines[0], lf_only_lines[0])
        issues.append(
            format_issue(
                filepath,
                first_mixed_line,
                "Inconsistent line endings",
            ),
        )

    # Check for trailing whitespace on non-blank lines only.
    for line_no, line in enumerate(content.split("\n"), 1):
        if line.strip() and line.rstrip() != line:
            issues.append(
                format_issue(filepath, line_no, "trailing whitespace"),
            )

    return issues


def verify_readme_consistency() -> bool:
    """Main verification function. Returns True if all checks pass."""
    args = parse_args()
    template_arg_path = Path(args.template)
    if template_arg_path.is_absolute():
        template_path = template_arg_path
        if not template_path.is_file():
            raise FileNotFoundError(f"Template not found: {template_path}")
        repo_root = find_repo_root_from_context(Path(os.getcwd()))
    else:
        template_relative_path = template_arg_path
        repo_root = find_repo_root(Path(os.getcwd()), template_relative_path)
        template_path = repo_root / template_relative_path

    template_headings = extract_heading_sequence(load_text(template_path))

    if not template_headings:
        print(f"WARN: Template {template_path} has no headings")
        return False

    readme_files = resolve_readme_files(repo_root, args.readme)
    if not readme_files:
        print("WARN: No README.md files found")
        return True

    all_issues: list[str] = []
    for readme in readme_files:
        issues = check_readme_format(readme, template_headings)
        if issues:
            all_issues.extend(issues)

    if all_issues:
        print("❌ README.md Format Verification Failed:")
        for issue in all_issues:
            print(f"  {issue}")
        return False

    if len(readme_files) == 1:
        readme_path = readme_files[0]
        head = f"✅ {readme_path} matches the template format from"
        msg = f"{head} {template_path}"
    else:
        msg = (
            f"✅ All {len(readme_files)} README.md files match the template "
            f"format from {template_path}"
        )
    print(msg)
    return True


if __name__ == "__main__":
    try:
        success = verify_readme_consistency()
        sys.exit(0 if success else 1)
    except BrokenPipeError:
        # Allow piping to tools like `head` without noisy tracebacks.
        sys.exit(0)
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)
