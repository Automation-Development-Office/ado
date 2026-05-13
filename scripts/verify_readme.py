#!/usr/bin/env python3
"""
Verify that all role README.md files conform to a standard format.

Uses roles/utilities_cron/README.md as the canonical template for:
- Section headings (Requirements, Variables, Usage, etc.)
- Structure and ordering
- Formatting conventions

Runs as:
  python scripts/verify_readme.py

Outputs:
  - Console messages indicating pass/fail
  - Exit code 0 on success, 1 on failure
"""

from __future__ import annotations

import os
import re
import sys

from pathlib import Path


TEMPLATE_RELATIVE_PATH = Path("roles") / "utilities_cron" / "README.md"
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$", re.MULTILINE)


def find_repo_root(start: Path) -> Path:
    """Find repository root by locating the template README path."""
    current = start.resolve()
    for candidate in [current, *current.parents]:
        if (candidate / TEMPLATE_RELATIVE_PATH).is_file():
            return candidate
    tpl_path = TEMPLATE_RELATIVE_PATH
    tpl_msg = f"Could not locate template README at {tpl_path}"
    raise FileNotFoundError(f"{tpl_msg} from {start}")


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


def load_text(path: Path) -> str:
    """Read UTF-8 content from a text file."""
    return path.read_text(encoding="utf-8")


def extract_heading_sequence(content: str) -> list[tuple[int, str]]:
    """Return heading tuples as (level, normalized_title) in document order."""
    headings: list[tuple[int, str]] = []
    for match in HEADING_RE.finditer(content):
        level = len(match.group(1))
        title = re.sub(r"\s+", " ", match.group(2).strip())
        headings.append((level, title))
    return headings


def validate_headings_against_template(
    filepath: Path,
    content: str,
    template_headings: list[tuple[int, str]],
) -> list[str]:
    """Ensure README contains template section headings in the same order."""
    issues: list[str] = []
    headings = extract_heading_sequence(content)

    if not headings:
        issues.append(f"{filepath}: Missing headings")
        return issues

    # First heading is role-specific. Validate shape, not exact text.
    first_level, first_title = headings[0]
    role_pattern = r"^Role:\s+`[^`]+`$"
    if first_level != 1 or not re.match(role_pattern, first_title):
        err = "First heading should match '# Role: `name`'"
        issues.append(f"{filepath}: {err}")

    # Match section/subsection structure from template, excluding H1 title.
    expected_sections = [h for h in template_headings if h[0] >= 2]
    position = 0
    for expected in expected_sections:
        found = False
        for i in range(position, len(headings)):
            if headings[i] == expected:
                found = True
                position = i + 1
                break
        if not found:
            heading_str = "#" * expected[0]
            heading_title = expected[1]
            err = f"Missing heading: {heading_str} {heading_title}"
            issues.append(f"{filepath}: {err}")

    return issues


def check_readme_format(
    filepath: Path,
    template_headings: list[tuple[int, str]],
) -> list[str]:
    """Verify README.md format and structure against the template."""
    content = load_text(filepath)
    issues: list[str] = []

    # Verify file starts with a main heading.
    if not re.match(r"^#\s+", content):
        issues.append(f"{filepath}: Missing main heading (# Title)")

    # Verify at least one subheading exists.
    if not re.search(r"^##\s+", content, re.MULTILINE):
        issues.append(f"{filepath}: Missing subheadings (## Section)")

    template_issues = validate_headings_against_template(
        filepath,
        content,
        template_headings,
    )
    issues.extend(template_issues)

    # Check for consistent line endings.
    if "\r\n" in content and "\n" in content.replace("\r\n", ""):
        issues.append(f"{filepath}: Inconsistent line endings")

    # Check for trailing whitespace on lines.
    for i, line in enumerate(content.split("\n"), 1):
        if line.rstrip() != line:
            issues.append(f"{filepath}: Line {i} has trailing whitespace")

    return issues


def verify_readme_consistency() -> bool:
    """Main verification function. Returns True if all checks pass."""
    repo_root = find_repo_root(Path(os.getcwd()))
    template_path = repo_root / TEMPLATE_RELATIVE_PATH
    template_headings = extract_heading_sequence(load_text(template_path))

    if not template_headings:
        print(f"WARN: Template {template_path} has no headings")
        return False

    readme_files = get_readme_files(repo_root)
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

    msg = (
        f"✅ All {len(readme_files)} README.md files match the template "
        f"format from {TEMPLATE_RELATIVE_PATH}"
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
