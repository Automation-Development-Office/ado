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
    role_pattern = r"^Role:\s+(`[^`]+`|[^\n`]+)$"
    if first_level != 1 or not re.match(role_pattern, first_title):
        err = "First heading should match '# Role: name' or '# Role: `name`'"
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

    # Check for trailing whitespace on non-blank lines only.
    for i, line in enumerate(content.split("\n"), 1):
        if line.strip() and line.rstrip() != line:
            issues.append(f"{filepath}: Line {i} has trailing whitespace")

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
