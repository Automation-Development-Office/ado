#!/usr/bin/env python3
"""Validate a release version string for antsibull-changelog."""

import os

from semantic_version import Version


def main() -> None:
    version = os.environ.get("CHECK_VERSION", "").strip()
    if not version:
        print("CHECK_VERSION environment variable is required.")
        raise SystemExit(1)

    try:
        Version(version)
    except ValueError as exc:
        print(f"Invalid release version '{version}' for antsibull-changelog.")
        print("Use semantic versioning such as 1.2.0-rc1 or 249.0.0-rc1.")
        print("Avoid versions like 249.0.0.1-rc1.")
        print(f"Details: {exc}")
        raise SystemExit(1) from exc


if __name__ == "__main__":
    main()
