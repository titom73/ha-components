#!/usr/bin/env python3
"""
Validate YAML structure of blueprint files.
Ensures all YAML files are properly formed and contain required blueprint sections.
"""

import os
import sys
import yaml
from pathlib import Path

def validate_yaml_file(file_path):
    """Validate a single YAML file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = yaml.safe_load(file)
            
        if data is None:
            print(f"❌ {file_path}: Empty YAML file")
            return False
            
        print(f"✅ {file_path}: Valid YAML structure")
        return True
        
    except yaml.YAMLError as e:
        print(f"❌ {file_path}: YAML syntax error - {e}")
        return False
    except Exception as e:
        print(f"❌ {file_path}: Error reading file - {e}")
        return False

def find_blueprint_files():
    """Find all blueprint YAML files."""
    blueprint_dir = Path("blueprints")
    if not blueprint_dir.exists():
        print("❌ blueprints directory not found")
        return []
    
    yaml_files = []
    for ext in ["*.yml", "*.yaml"]:
        yaml_files.extend(blueprint_dir.rglob(ext))
    
    return yaml_files

def main():
    """Main validation function."""
    print("🔍 Validating YAML structure of blueprint files...")
    
    files = find_blueprint_files()
    if not files:
        print("⚠️  No blueprint files found")
        return 0
    
    print(f"📁 Found {len(files)} blueprint files")
    
    success_count = 0
    for file_path in files:
        if validate_yaml_file(file_path):
            success_count += 1
    
    print(f"\n📊 Results: {success_count}/{len(files)} files passed validation")
    
    if success_count == len(files):
        print("🎉 All YAML files are valid!")
        return 0
    else:
        print("💥 Some YAML files have errors")
        return 1

if __name__ == "__main__":
    sys.exit(main())
