# infra.ado.manage_vm_image

This Ansible role creates a qcow2 virtual machine image from an existing base image.
It runs prerequisite setup, validates paths, inspects the base image with qemu-img info,
and creates the output image with qemu-img convert.

## Role Information

| Property                | Value                         |
| ----------------------- | ----------------------------- |
| Author                  | Automation Development Office |
| License                 | GPL-3.0-or-later              |
| Minimum Ansible Version | 2.14                          |

## Options

### `manage_vm_image_action` (str) (required)

Action selector used by the prerequisite and assertion tasks. The active workflow expects 'create'.

### `manage_vm_image_dest_path` (str) (required)

Destination path for the output image. In prerequisites, this is expanded to the final output image path by appending manage_vm_image_dest_name.

### `manage_vm_image_dest_name` (str) (required)

Output image file name appended to manage_vm_image_dest_path in prerequisites.

### `manage_vm_image_base_path` (str) (required)

Base image directory input. In prerequisites, this is expanded to the final base image path by appending manage_vm_image_base_name.

### `manage_vm_image_base_name` (str) (required)

Base image file name appended to manage_vm_image_base_path in prerequisites.

### `manage_vm_image_format` (str)

Output image format passed to qemu-img convert -O.

**Default:** `qcow2`

### `manage_vm_image_download` (bool)

When false, the current create workflow runs. Download flow remains present but commented out in main.yml.

**Default:** `False`

### `manage_vm_image_path` (str)

Reserved default variable for a full destination path. It is defined in defaults but is not used by the current task flow.

### `manage_vm_image_size` (str)

Reserved for future image sizing workflows. Not used by the current task flow.

### `manage_vm_image_force` (bool)

Reserved for future replacement behavior. Not used by the current task flow.

**Default:** `False`

### `manage_vm_image_resize` (bool)

Reserved for a future post-create resize workflow. main.yml currently includes a TODO for this feature.

**Default:** `False`

### `manage_vm_image_backing` (bool)

Legacy variable from the earlier workflow. Not used by the current task flow.

**Default:** `True`

## See Also

See the role [README.md](../../roles/manage_vm_image/README.md) for more details.
