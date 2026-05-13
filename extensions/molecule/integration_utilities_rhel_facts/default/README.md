utilities_rhel_facts — Molecule Testing Guide
Overview

This document explains how Molecule is used to test the rhel_facts Ansible role. The role is designed to gather, validate, and expose Red Hat Enterprise Linux–specific system facts. Molecule provides a repeatable, automated workflow to ensure the role behaves consistently across supported RHEL versions and environments.
Testing Framework

The test suite uses:

    Molecule — scenario-based role testing

    Testinfra — Python assertions for system state validation

    Ansible Lint — static analysis for role quality

    Docker or Podman — ephemeral test instances

Each scenario validates that the role collects expected facts, exposes them correctly, and handles OS‑specific differences.
Directory Structure
Code

utilities_rhel_facts/
├── molecule/
│   └── default/
│       ├── converge.yml
│       ├── molecule.yml
│       ├── prepare.yml
│       └── tests/
│           └── test_rhel_facts.py

Key Files

    molecule.yml — defines platforms, drivers, and test sequence

    prepare.yml — optional setup tasks (package installs, repo config)

    converge.yml — applies the rhel_facts role

    test_rhel_facts.py — Testinfra tests validating collected facts

Running Tests
Full Test Run
Code

molecule test

Runs linting, dependency resolution, create → converge → verify → destroy.
Step-by-Step Execution

Useful for debugging:
Code

molecule create
molecule converge
molecule verify
molecule destroy

Linting Only
Code

molecule lint

What the Tests Validate

The Molecule suite ensures that:

    RHEL fact gathering completes without errors

    Expected custom facts are present in ansible_facts

    OS version detection logic behaves correctly across RHEL variants

    The role remains idempotent

    No deprecated modules or patterns are used

    The role works on all configured platforms (e.g., RHEL 8, RHEL 9)

Example Testinfra Assertions
python

def test_rhel_major_version(host):
    facts = host.ansible("setup")["ansible_facts"]
    assert "ansible_distribution_major_version" in facts
    assert facts["ansible_distribution"] == "RedHat"

Supported Platforms

Defined in molecule.yml, typically:

    RHEL 8.x

    RHEL 9.x

    Rocky Linux / AlmaLinux (optional compatibility)

Contributing

When adding new facts or logic:

    Update the Molecule scenario to reflect new behavior

    Add or modify Testinfra tests

    Run molecule test before submitting changes

    Ensure idempotency and linting pass


