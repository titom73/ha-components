#!/usr/bin/env python3
"""
Validate blueprint schema compliance.
Ensures all blueprint files follow Home Assistant blueprint schema requirements.
"""

import sys
import yaml
from pathlib import Path
from typing import Dict, List, Any


class HomeAssistantLoader(yaml.SafeLoader):
    """Custom YAML loader that handles Home Assistant specific tags."""
    pass


def construct_input(loader, node):
    """Handle !input tags in Home Assistant blueprints."""
    return f"!input {loader.construct_scalar(node)}"


def construct_include(loader, node):
    """Handle !include tags in Home Assistant configuration."""
    return f"!include {loader.construct_scalar(node)}"


def construct_include_dir_merge_list(loader, node):
    """Handle !include_dir_merge_list tags."""
    return f"!include_dir_merge_list {loader.construct_scalar(node)}"


# Add constructors for Home Assistant specific tags
HomeAssistantLoader.add_constructor('!input', construct_input)
HomeAssistantLoader.add_constructor('!include', construct_include)
HomeAssistantLoader.add_constructor('!include_dir_merge_list',
                                  construct_include_dir_merge_list)
HomeAssistantLoader.add_constructor('!secret', construct_include)


def validate_blueprint_structure(data: Dict[str, Any], file_path: str) -> bool:
    """Validate blueprint structure against Home Assistant requirements."""
    errors = []

    # Check for required top-level 'blueprint' key
    if 'blueprint' not in data:
        errors.append("Missing required 'blueprint' section")
        return False

    blueprint = data['blueprint']

    # Check required blueprint fields
    required_fields = ['name', 'description', 'domain']
    for field in required_fields:
        if field not in blueprint:
            errors.append(f"Missing required blueprint field: '{field}'")

    # Validate domain
    if 'domain' in blueprint:
        valid_domains = ['automation', 'script']
        if blueprint['domain'] not in valid_domains:
            errors.append(f"Invalid domain: {blueprint['domain']}. "
                        f"Must be one of: {valid_domains}")

    # Check for input section structure
    if 'input' in blueprint:
        if not isinstance(blueprint['input'], dict):
            errors.append("Blueprint 'input' section must be a dictionary")
        else:
            for input_name, input_config in blueprint['input'].items():
                if not isinstance(input_config, dict):
                    errors.append(f"Input '{input_name}' must be a dictionary")
                    continue

                # Check required input fields
                if 'name' not in input_config:
                    errors.append(f"Input '{input_name}' missing required 'name' field")

                # Validate selector if present
                if 'selector' in input_config:
                    validate_selector(input_config['selector'], input_name, errors)

    # Check for automation-specific fields if domain is automation
    if blueprint.get('domain') == 'automation':
        required_auto_fields = ['trigger', 'action']
        for field in required_auto_fields:
            if field not in data:
                errors.append(f"Missing required automation field: '{field}'")

    if errors:
        for error in errors:
            print(f"❌ {file_path}: {error}")
        return False

    print(f"✅ {file_path}: Valid blueprint schema")
    return True


def validate_selector(selector: Dict[str, Any], input_name: str,
                     errors: List[str]) -> None:
    """Validate input selector configuration."""
    if not isinstance(selector, dict):
        errors.append(f"Input '{input_name}' selector must be a dictionary")
        return

    if len(selector) != 1:
        errors.append(f"Input '{input_name}' selector must have exactly one type")
        return

    selector_type = list(selector.keys())[0]
    valid_selectors = [
        'entity', 'number', 'boolean', 'time', 'date', 'datetime',
        'text', 'select', 'action', 'area', 'device', 'duration',
        'icon', 'media', 'object', 'target', 'template', 'theme',
        'color_rgb', 'color_temp', 'location'
    ]

    if selector_type not in valid_selectors:
        errors.append(f"Input '{input_name}' has invalid selector type: "
                     f"{selector_type}")


def validate_blueprint_file(file_path: Path) -> bool:
    """Validate a single blueprint file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = yaml.load(file, Loader=HomeAssistantLoader)

        if data is None:
            print(f"❌ {file_path}: Empty YAML file")
            return False

        return validate_blueprint_structure(data, str(file_path))

    except yaml.YAMLError as e:
        print(f"❌ {file_path}: YAML syntax error - {e}")
        return False
    except Exception as e:
        print(f"❌ {file_path}: Error reading file - {e}")
        return False


def find_blueprint_files() -> List[Path]:
    """Find all blueprint YAML files."""
    blueprint_dir = Path("blueprints")
    if not blueprint_dir.exists():
        print("❌ blueprints directory not found")
        return []

    yaml_files = []
    for ext in ["*.yml", "*.yaml"]:
        yaml_files.extend(blueprint_dir.rglob(ext))

    return yaml_files


def main() -> int:
    """Main validation function."""
    print("🔍 Validating blueprint schema compliance...")

    files = find_blueprint_files()
    if not files:
        print("⚠️  No blueprint files found")
        return 0

    print(f"📁 Found {len(files)} blueprint files")

    success_count = 0
    for file_path in files:
        if validate_blueprint_file(file_path):
            success_count += 1

    print(f"\n📊 Results: {success_count}/{len(files)} files passed validation")

    if success_count == len(files):
        print("🎉 All blueprint files are valid!")
        return 0
    else:
        print("💥 Some blueprint files have schema errors")
        return 1


if __name__ == "__main__":
    sys.exit(main())
