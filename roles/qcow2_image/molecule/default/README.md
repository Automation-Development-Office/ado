# Molecule Scenario: `default`

This scenario validates the current `vm_image` role workflow by creating a temporary local qcow2 base image, running the role to produce a cloned qcow2 image, and verifying that the destination image exists and reports the expected format.

## What It Tests

- `pre_reqs.yml` expands the base and destination paths correctly.
- `assertions.yml` accepts the provided create inputs.
- `create_qcow_from_base.yml` creates a qcow2 image from a local base image.
- `verify.yml` confirms the output image exists, is non-empty, and is in `qcow2` format.

## Scenario Files

- `molecule.yml`: Scenario configuration and test sequence.
- `converge.yml`: Creates a temporary base image and applies the role.
- `verify.yml`: Validates the created image.
- `destroy.yml`: Removes the temporary test artifacts under `/tmp/vm_image_molecule`.

## Notes

- This scenario uses `ansible_connection: local` and runs against `molecule-localhost`.
- It requires `qemu-img` to be installed on the test host.
- Temporary test files are created under `/tmp/vm_image_molecule` and removed during `destroy`.