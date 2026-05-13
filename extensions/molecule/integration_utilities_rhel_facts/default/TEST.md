Molecule Test Documentation — utilities_rhel_facts Role
Purpose

This document describes the testing approach for the rhel_facts Ansible role using Molecule and Testinfra.
The goal is to ensure the role reliably gathers and exposes RHEL‑specific system facts across supported platforms.
Test Layout
Code

molecule/
└── default/
    ├── converge.yml
    ├── molecule.yml
    ├── prepare.yml
    └── tests/
        └── test_rhel_facts.py

Components

    molecule.yml — defines platforms, drivers, and test sequence

    prepare.yml — installs prerequisites before running the role

    converge.yml — applies the rhel_facts role

    test_rhel_facts.py — Testinfra tests validating fact collection

Test Execution
Full Test Cycle
Code

molecule test

Runs lint → create → prepare → converge → verify → destroy.
Individual Steps

Useful for debugging:
Code

molecule create
molecule prepare
molecule converge
molecule verify
molecule destroy

Linting
Code

molecule lint

What the Tests Validate

    RHEL fact gathering runs without errors

    Custom facts are added to ansible_facts

    Distribution and version detection logic is correct

    Role is idempotent

    Behavior is consistent across configured platforms (RHEL 8, RHEL 9, Rocky/Alma optional)



Supported Platforms

Defined in molecule.yml:

    RHEL 8.x

    RHEL 9.x

    Rocky Linux / AlmaLinux (optional)


