#!/usr/bin/env python3
"""
Generate RST documentation for Ansible roles from argument_specs.yml files.
"""

import os
import sys
import yaml
from pathlib import Path
from typing import Dict, Any, Optional

def load_argument_specs(role_path: Path) -> Optional[Dict[str, Any]]:
    """Load argument_specs.yml from a role."""
    specs_file = role_path / "meta" / "argument_specs.yml"
    if not specs_file.exists():
        return None
    
    with open(specs_file, 'r') as f:
        try:
            return yaml.safe_load(f)
        except yaml.YAMLError as e:
            print(f"Error parsing {specs_file}: {e}", file=sys.stderr)
            return None

def load_role_meta(role_path: Path) -> Optional[Dict[str, Any]]:
    """Load meta/main.yml from a role."""
    meta_file = role_path / "meta" / "main.yml"
    if not meta_file.exists():
        return None
    
    with open(meta_file, 'r') as f:
        try:
            return yaml.safe_load(f)
        except yaml.YAMLError as e:
            print(f"Error parsing {meta_file}: {e}", file=sys.stderr)
            return None

def generate_role_md(role_name: str, role_path: Path, collection_name: str) -> Optional[str]:
    """Generate Markdown documentation for a single role."""
    specs = load_argument_specs(role_path)
    meta = load_role_meta(role_path)
    
    if not specs or "argument_specs" not in specs:
        print(f"Warning: {role_name} has no valid argument_specs.yml", file=sys.stderr)
        return None
    
    main_spec = specs.get("argument_specs", {}).get("main", {})
    if not main_spec:
        print(f"Warning: {role_name} has no 'main' argument spec", file=sys.stderr)
        return None
    
    # Get role description
    description = main_spec.get("description", "")
    short_description = main_spec.get("short_description", "")
    if not description:
        description = short_description
    
    # Get galaxy info
    galaxy_info = {}
    if meta and "galaxy_info" in meta:
        galaxy_info = meta["galaxy_info"]
    
    author = galaxy_info.get("author", "Unknown")
    license_val = galaxy_info.get("license", "Unknown")
    min_ansible = galaxy_info.get("min_ansible_version", "2.9")
    
    # Build Markdown content
    lines = []
    
    # Title
    role_title = f"{collection_name}.{role_name}"
    lines.append(f"# {role_title}")
    lines.append("")
    
    # Description
    if description:
        lines.append(description)
        lines.append("")
    
    # Metadata table
    lines.append("## Role Information")
    lines.append("")
    lines.append("| Property | Value |")
    lines.append("|----------|-------|")
    lines.append(f"| Author | {author} |")
    lines.append(f"| License | {license_val} |")
    lines.append(f"| Minimum Ansible Version | {min_ansible} |")
    lines.append("")
    
    # Arguments/Options
    options = main_spec.get("options", {})
    if options:
        lines.append("## Options")
        lines.append("")
        
        for option_name, option_info in options.items():
            option_type = option_info.get("type", "str")
            required = option_info.get("required", False)
            default = option_info.get("default", None)
            option_desc = option_info.get("description", "")
            choices = option_info.get("choices", [])
            
            # Option header
            req_str = " (required)" if required else ""
            lines.append(f"### `{option_name}` ({option_type}){req_str}")
            lines.append("")
            
            # Option description
            if option_desc:
                lines.append(option_desc)
                lines.append("")
            
            # Default value
            if default is not None:
                lines.append(f"**Default:** `{default}`")
                lines.append("")
            
            # Choices
            if choices:
                lines.append("**Choices:**")
                for choice in choices:
                    lines.append(f"- `{choice}`")
                lines.append("")
    
    # Examples from role
    readme_path = role_path / "README.md"
    if readme_path.exists():
        lines.append("## See Also")
        lines.append("")
        lines.append(f"See the role [README.md](../../roles/{role_name}/README.md) for more details.")
        lines.append("")
    
    return "\n".join(lines)

def main():
    """Main entry point."""
    # Get paths
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent
    roles_dir = repo_root / "roles"
    docs_dir = repo_root / "docs"
    roles_docs_dir = docs_dir / "roles"
    
    # Ensure docs directory exists
    roles_docs_dir.mkdir(parents=True, exist_ok=True)
    
    # Get collection name from galaxy.yml
    galaxy_file = repo_root / "galaxy.yml"
    collection_name = "ado"
    if galaxy_file.exists():
        with open(galaxy_file, 'r') as f:
            try:
                galaxy = yaml.safe_load(f)
                namespace = galaxy.get("namespace", "infra")
                name = galaxy.get("name", "ado")
                collection_name = f"{namespace}.{name}"
            except yaml.YAMLError:
                pass
    
    # Find all roles
    if not roles_dir.exists():
        print("No roles directory found")
        return 0
    
    roles = [d for d in roles_dir.iterdir() if d.is_dir() and (d / "meta").exists()]
    
    if not roles:
        print("No roles with meta directory found")
        return 0
    
    # Generate documentation for each role
    generated_docs = []
    for role_path in sorted(roles):
        role_name = role_path.name
        print(f"Generating documentation for role: {role_name}")
        
        md_content = generate_role_md(role_name, role_path, collection_name)
        if md_content:
            output_file = roles_docs_dir / f"{role_name}_role.md"
            with open(output_file, 'w') as f:
                f.write(md_content)
            print(f"  → {output_file}")
            generated_docs.append((role_name, role_path))
    
    # Generate index
    if generated_docs:
        index_lines = []
        index_lines.append("# Roles")
        index_lines.append("")
        
        for role_name, _ in generated_docs:
            index_lines.append(f"- [{role_name}](roles/{role_name}_role.md)")
        
        index_lines.append("")
        
        index_file = docs_dir / "roles.md"
        with open(index_file, 'w') as f:
            f.write("\n".join(index_lines))
        print(f"Generated role index: {index_file}")
    
    print(f"\nGenerated documentation for {len(generated_docs)} role(s)")
    return 0

if __name__ == "__main__":
    sys.exit(main())
