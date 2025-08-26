#!/usr/bin/env python3
"""
Test blueprint imports in Home Assistant environment.
Simulates importing blueprints into a Home Assistant instance.
"""

import sys
import yaml
import tempfile
import shutil
from pathlib import Path
from typing import Dict, List, Any


def create_test_config() -> str:
    """Create a minimal Home Assistant configuration for testing."""
    config_content = """
homeassistant:
  name: Test
  latitude: 0
  longitude: 0
  elevation: 0
  unit_system: metric
  time_zone: UTC

automation: !include_dir_merge_list automations/
script: !include_dir_merge_list scripts/

logger:
  default: warning
"""
    return config_content


def test_blueprint_import(blueprint_path: Path, config_dir: Path) -> bool:
    """Test if a blueprint can be imported."""
    try:
        with open(blueprint_path, 'r', encoding='utf-8') as file:
            blueprint_data = yaml.safe_load(file)

        if not blueprint_data or 'blueprint' not in blueprint_data:
            print(f"❌ {blueprint_path}: Invalid blueprint structure")
            return False

        # Create blueprint directory structure
        blueprint_dir = config_dir / "blueprints" / "automation"
        blueprint_dir.mkdir(parents=True, exist_ok=True)

        # Copy blueprint file
        target_file = blueprint_dir / blueprint_path.name
        shutil.copy2(blueprint_path, target_file)

        # Try to validate the blueprint can be loaded
        with open(target_file, 'r', encoding='utf-8') as file:
            loaded_data = yaml.safe_load(file)

        if loaded_data == blueprint_data:
            print(f"✅ {blueprint_path}: Successfully imported")
            return True
        else:
            print(f"❌ {blueprint_path}: Data mismatch after import")
            return False

    except Exception as e:
        print(f"❌ {blueprint_path}: Import failed - {e}")
        return False


def validate_blueprint_inputs(blueprint_data: Dict[str, Any]) -> List[str]:
    """Validate blueprint inputs for common issues."""
    issues = []

    if 'blueprint' not in blueprint_data:
        return ["Missing blueprint section"]

    blueprint = blueprint_data['blueprint']

    if 'input' not in blueprint:
        return issues  # No inputs to validate

    inputs = blueprint['input']

    for input_name, input_config in inputs.items():
        # Check for required name field
        if 'name' not in input_config:
            issues.append(f"Input '{input_name}' missing name field")

        # Check selector configuration
        if 'selector' in input_config:
            selector = input_config['selector']
            if not isinstance(selector, dict) or len(selector) != 1:
                issues.append(f"Input '{input_name}' has invalid selector")

        # Check for default values where appropriate
        if input_config.get('selector', {}).get('boolean') is not None:
            if 'default' not in input_config:
                issues.append(f"Boolean input '{input_name}' should have "
                            "default value")

    return issues


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
    """Main testing function."""
    print("🧪 Testing blueprint imports...")

    files = find_blueprint_files()
    if not files:
        print("⚠️  No blueprint files found")
        return 0

    print(f"📁 Found {len(files)} blueprint files")

    # Create temporary configuration directory
    with tempfile.TemporaryDirectory() as temp_dir:
        config_dir = Path(temp_dir)

        # Create test configuration
        config_file = config_dir / "configuration.yaml"
        with open(config_file, 'w') as f:
            f.write(create_test_config())

        success_count = 0
        for file_path in files:
            # Test basic import
            if test_blueprint_import(file_path, config_dir):
                # Validate inputs
                try:
                    with open(file_path, 'r', encoding='utf-8') as file:
                        blueprint_data = yaml.safe_load(file)

                    issues = validate_blueprint_inputs(blueprint_data)
                    if issues:
                        print(f"⚠️  {file_path}: Input issues found:")
                        for issue in issues:
                            print(f"   - {issue}")

                    success_count += 1
                except Exception as e:
                    print(f"❌ {file_path}: Validation error - {e}")

    print(f"\n📊 Results: {success_count}/{len(files)} blueprints "
          "imported successfully")

    if success_count == len(files):
        print("🎉 All blueprints imported successfully!")
        return 0
    else:
        print("💥 Some blueprints failed to import")
        return 1


if __name__ == "__main__":
    sys.exit(main())
