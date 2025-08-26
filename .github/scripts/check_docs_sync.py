#!/usr/bin/env python3
"""
Check documentation synchronization with blueprints.
Ensures documentation exists for all blueprints and is up to date.
"""

import sys
import yaml
from pathlib import Path
from typing import Dict, List


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


def find_blueprint_files() -> List[Path]:
    """Find all blueprint YAML files."""
    blueprint_dir = Path("blueprints")
    if not blueprint_dir.exists():
        return []

    yaml_files = []
    for ext in ["*.yml", "*.yaml"]:
        yaml_files.extend(blueprint_dir.rglob(ext))

    return yaml_files


def find_documentation_files() -> List[Path]:
    """Find all documentation markdown files."""
    docs_dir = Path("docs")
    if not docs_dir.exists():
        return []

    return list(docs_dir.glob("*.md"))


def extract_blueprint_info(blueprint_path: Path) -> Dict[str, str]:
    """Extract key information from a blueprint file."""
    try:
        with open(blueprint_path, 'r', encoding='utf-8') as file:
            data = yaml.load(file, Loader=HomeAssistantLoader)

        if not data or 'blueprint' not in data:
            return {}

        blueprint = data['blueprint']
        return {
            'name': blueprint.get('name', ''),
            'description': blueprint.get('description', ''),
            'domain': blueprint.get('domain', ''),
            'file_path': str(blueprint_path)
        }
    except Exception:
        return {}


def check_documentation_exists(blueprint_files: List[Path],
                               doc_files: List[Path]) -> Dict[str, bool]:
    """Check if documentation exists for each blueprint."""
    results = {}

    # Create a set of documentation file stems for quick lookup
    doc_stems = {doc.stem for doc in doc_files}

    for blueprint_path in blueprint_files:
        # Generate expected documentation filename
        relative_path = blueprint_path.relative_to(Path("blueprints"))
        expected_doc_name = str(relative_path).replace('/', '-').replace('.yml', '').replace('.yaml', '')

        # Check if documentation exists
        has_docs = expected_doc_name in doc_stems
        results[str(blueprint_path)] = has_docs

        if has_docs:
            print(f"✅ {blueprint_path}: Documentation exists")
        else:
            print(f"❌ {blueprint_path}: Missing documentation "
                  f"(expected: docs/{expected_doc_name}.md)")

    return results


def check_documentation_completeness(blueprint_files: List[Path]) -> bool:
    """Check if documentation covers all blueprint features."""
    all_complete = True

    for blueprint_path in blueprint_files:
        blueprint_info = extract_blueprint_info(blueprint_path)
        if not blueprint_info:
            continue

        # Generate expected documentation path
        relative_path = blueprint_path.relative_to(Path("blueprints"))
        doc_name = str(relative_path).replace('/', '-').replace('.yml', '').replace('.yaml', '')
        doc_path = Path(f"docs/{doc_name}.md")

        if not doc_path.exists():
            continue

        try:
            with open(doc_path, 'r', encoding='utf-8') as file:
                doc_content = file.read().lower()

            # Check for essential documentation sections
            required_sections = [
                'overview',
                'configuration',
                'setup',
                'usage',
                'troubleshooting'
            ]

            missing_sections = []
            for section in required_sections:
                if section not in doc_content:
                    missing_sections.append(section)

            if missing_sections:
                print(f"⚠️  {doc_path}: Missing sections: "
                      f"{', '.join(missing_sections)}")
                all_complete = False
            else:
                print(f"✅ {doc_path}: Complete documentation")

        except Exception as e:
            print(f"❌ {doc_path}: Error reading documentation - {e}")
            all_complete = False

    return all_complete


def check_readme_index() -> bool:
    """Check if README.md properly indexes all blueprints."""
    readme_path = Path("docs/README.md")
    if not readme_path.exists():
        print("❌ docs/README.md not found")
        return False

    try:
        with open(readme_path, 'r', encoding='utf-8') as file:
            readme_content = file.read()

        # Find all blueprint files
        blueprint_files = find_blueprint_files()

        missing_links = []
        for blueprint_path in blueprint_files:
            relative_path = blueprint_path.relative_to(Path("blueprints"))
            doc_name = str(relative_path).replace('/', '-').replace('.yml', '').replace('.yaml', '')

            # Check if the documentation file is linked in README
            if f"({doc_name}.md)" not in readme_content:
                missing_links.append(doc_name)

        if missing_links:
            print(f"⚠️  docs/README.md: Missing links to: "
                  f"{', '.join(missing_links)}")
            return False
        else:
            print("✅ docs/README.md: All blueprints properly indexed")
            return True

    except Exception as e:
        print(f"❌ docs/README.md: Error reading file - {e}")
        return False


def main() -> int:
    """Main documentation sync check."""
    print("📚 Checking documentation synchronization...")

    blueprint_files = find_blueprint_files()
    doc_files = find_documentation_files()

    if not blueprint_files:
        print("⚠️  No blueprint files found")
        return 0

    print(f"📁 Found {len(blueprint_files)} blueprint files")
    print(f"📄 Found {len(doc_files)} documentation files")

    # Check if documentation exists for all blueprints
    doc_exists = check_documentation_exists(blueprint_files, doc_files)

    # Check documentation completeness
    docs_complete = check_documentation_completeness(blueprint_files)

    # Check README index
    readme_ok = check_readme_index()

    # Summary
    total_blueprints = len(blueprint_files)
    documented_blueprints = sum(doc_exists.values())

    print(f"\n📊 Documentation Coverage: "
          f"{documented_blueprints}/{total_blueprints} blueprints")

    if documented_blueprints == total_blueprints and docs_complete and readme_ok:
        print("🎉 All documentation is synchronized!")
        return 0
    else:
        print("💥 Documentation synchronization issues found")
        return 1


if __name__ == "__main__":
    sys.exit(main())
