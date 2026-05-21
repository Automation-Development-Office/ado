# Role: platform_ec2

Creates an EC2 instance, creates a snapshot from the attached EBS device, and creates an AMI from that instance.

## Requirements

- Ansible `2.18` or newer.
- `amazon.aws` collection available (modules used: `ec2_instance`, `ec2_snapshot`, `ec2_ami`).
- AWS credentials with permissions to create/manage EC2 instances, snapshots, and AMIs.
- Python AWS SDK dependencies available to Ansible (`boto3` and `botocore`).

## Variables

All role variables are currently defined in `vars/main.yml`.

| Variable | Default | Required | Description |
| --- | --- | --- | --- |
| `instance_name` | `""` | yes | Name for the EC2 instance created by the role. |
| `aws_access_key` | `""` | yes | AWS access key ID used by the AWS modules. |
| `aws_secret_key` | `""` | yes | AWS secret key used by the AWS modules. |
| `image_id` | `""` | yes | Source AMI ID for the instance launch. |
| `vpc_subnet_id` | `""` | no | VPC subnet ID passed to `ec2_instance`. |
| `region` | `"us-east-1"` | no | AWS region used for all module calls. |
| `instance_type` | `"t3.micro"` | no | EC2 instance type to launch. |
| `key_name` | `""` | yes | EC2 key pair name for SSH access. |
| `security_group` | `""` | yes | Security group assigned at instance launch. |
| `subnet_id` | `""` | no | Additional subnet field passed to `ec2_instance`. |
| `volume_device_name` | `"/dev/xvdf"` | no | EBS device name used for create/snapshot steps. |
| `volume_size` | `8` | no | Size (GiB) for the attached EBS volume. |
| `volume_delete_on_termination` | `true` | no | Whether the EBS volume is deleted at termination. |
| `snapshot_description` | `"Snapshot created by platform_ec2 role"` | no | Description for the created snapshot. |
| `new_instance_name` | `""` | yes | Name for the AMI created from the launched instance. |
| `name_tag` | `""` | no | Value used for the AMI `Name` tag. |

## Role Behavior

The role performs these actions in order:

1. Launches an EC2 instance with an attached EBS volume.
2. Extracts the created instance ID.
3. Creates an EBS snapshot from `volume_device_name`.
4. Extracts the created snapshot ID.
5. Creates an AMI from the launched instance.

## Facts Set By Role

- `platform_ec2_instance_id`: instance ID created by `ec2_instance`.
- `platform_ec2_snapshot_id`: snapshot ID created by `ec2_snapshot`.

## Example Playbook

```yaml
- hosts: localhost
  gather_facts: false
  roles:
    - role: platform_ec2
      vars:
        instance_name: "platform-ec2-build-host"
        aws_access_key: "{{ lookup('env', 'AWS_ACCESS_KEY_ID') }}"
        aws_secret_key: "{{ lookup('env', 'AWS_SECRET_ACCESS_KEY') }}"
        image_id: "ami-0123456789abcdef0"
        vpc_subnet_id: "subnet-0123456789abcdef0"
        region: "us-east-1"
        instance_type: "t3.medium"
        key_name: "platform-keypair"
        security_group: "sg-0123456789abcdef0"
        subnet_id: "subnet-0123456789abcdef0"
        volume_device_name: "/dev/xvdf"
        volume_size: 16
        volume_delete_on_termination: true
        snapshot_description: "Golden image build snapshot"
        new_instance_name: "platform-ec2-golden-ami"
        name_tag: "platform-ec2-golden-ami"
```

## License

GPL-3.0-or-later

## Author

Services Team
