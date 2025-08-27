# Blueprint Validation System

This directory contains automated validation tools for Home Assistant blueprints stored in this repository.

## Overview

The validation system ensures that:
- ✅ All YAML files have correct syntax
- ✅ Blueprints follow Home Assistant schema requirements
- ✅ Blueprints can be imported into Home Assistant
- ✅ Documentation exists and is synchronized
- ✅ Security best practices are followed

## Validation Levels

### 1. YAML Syntax Validation
**Script**: `validate_yaml_structure.py`
**Purpose**: Ensures all YAML files are properly formatted and parseable

**Checks**:
- Valid YAML syntax
- Proper encoding (UTF-8)
- File accessibility

**Example error**:
```
❌ blueprints/climate/cover-heat-management.yml: YAML syntax error - expected <block end>, but found '<scalar>'
```

### 2. Blueprint Schema Validation
**Script**: `validate_blueprint_schema.py`
**Purpose**: Validates blueprint structure against Home Assistant requirements

**Checks**:
- Required blueprint sections (`name`, `description`, `domain`)
- Valid domain values (`automation`, `script`)
- Input parameter structure and types
- Selector configuration validity

**Example error**:
```
❌ blueprints/notifications/camera-snapshot.yml: Missing required blueprint field: 'domain'
```

### 3. Blueprint Import Testing
**Script**: `test_blueprint_imports.py`
**Purpose**: Simulates importing blueprints into a Home Assistant environment

**Checks**:
- Blueprint can be loaded by Home Assistant
- Input validation logic
- Template syntax (basic check)
- Default value presence for boolean inputs

**Example error**:
```
❌ blueprints/climate/cover-heat-management.yml: Boolean input 'sun_filter_enabled' should have default value
```

### 4. Documentation Synchronization
**Script**: `check_docs_sync.py`
**Purpose**: Ensures documentation exists for all blueprints and is complete

**Checks**:
- Documentation file exists for each blueprint
- Required documentation sections present
- README.md properly indexes all blueprints
- Documentation filename conventions

**Example error**:
```
❌ blueprints/notifications/camera-snapshot.yml: Missing documentation (expected: docs/notifications-camera-snapshot.md)
```

## GitHub Actions Workflows

### Basic Validation (`blueprint-basic-validation.yml`)
Runs on every push and pull request affecting blueprint files:
1. YAML syntax validation with yamllint
2. Blueprint schema validation
3. Documentation synchronization check

### Full Validation (`blueprint-validation.yml`)
Comprehensive validation including:
1. All basic validation steps
2. Home Assistant configuration check
3. Blueprint import simulation
4. Security scanning with Trivy

## Local Testing

### Quick Test
```bash
# Make the script executable
chmod +x test-blueprints.sh

# Run all validation tests
./test-blueprints.sh
```

### Individual Tests
```bash
# Install dependencies
pip install pyyaml yamllint

# Test YAML syntax
yamllint blueprints/

# Test blueprint schema
python3 .github/scripts/validate_blueprint_schema.py

# Test imports
python3 .github/scripts/test_blueprint_imports.py

# Check documentation
python3 .github/scripts/check_docs_sync.py
```

## Configuration Files

### `.yamllint.yml`
yamllint configuration optimized for Home Assistant blueprints:
- Relaxed mode for flexibility
- 120 character line length limit
- Allows Home Assistant specific constructs

### `test_configuration.yaml`
Minimal Home Assistant configuration for testing:
- Mock entities for all blueprint types
- Template sensors for testing
- Required integrations (camera, telegram_bot, etc.)

## Common Issues and Solutions

### YAML Syntax Errors
**Problem**: Invalid YAML structure
**Solution**: Use a YAML validator or IDE with YAML support
**Prevention**: Enable yamllint in your editor

### Missing Blueprint Fields
**Problem**: Required blueprint metadata missing
**Solution**: Add required fields (`name`, `description`, `domain`)
**Prevention**: Use the blueprint template structure

### Input Validation Issues
**Problem**: Invalid selector configuration
**Solution**: Check Home Assistant selector documentation
**Prevention**: Test selectors in Home Assistant UI

### Documentation Sync Issues
**Problem**: Documentation missing or incomplete
**Solution**: Create documentation following the template in `docs/`
**Prevention**: Update documentation when modifying blueprints

## Blueprint Naming Conventions

### File Naming
- Use lowercase with hyphens: `camera-snapshot-to-telegram.yml`
- Include domain prefix: `automation-` for automation blueprints
- Be descriptive but concise

### Documentation Naming
- Match blueprint path: `blueprints/notifications/camera-snapshot.yml` → `docs/notifications-camera-snapshot.md`
- Use hyphens to replace path separators

## Security Considerations

### Validated Elements
- No hardcoded credentials or sensitive data
- Proper input validation and sanitization
- Safe template usage without code injection risks
- File path validation for security

### Best Practices
- Use secrets for sensitive configuration
- Validate all user inputs
- Avoid dynamic code execution in templates
- Regular security scanning with Trivy

## Extending the Validation System

### Adding New Checks
1. Create a new Python script in `.github/scripts/`
2. Follow the existing pattern with clear output formatting
3. Add to the GitHub Actions workflow
4. Update the local test script

### Custom Validations
Example: Check for required automation modes
```python
def validate_automation_mode(blueprint_data):
    if blueprint_data.get('mode') not in ['single', 'restart', 'queued']:
        return False, "Missing or invalid automation mode"
    return True, "Valid automation mode"
```

## Troubleshooting

### GitHub Actions Failing
1. Check the Actions tab in your repository
2. Review the specific failing step
3. Run the same validation locally
4. Fix issues and push again

### Local Test Failures
1. Ensure Python 3.7+ is installed
2. Install required dependencies: `pip install pyyaml yamllint`
3. Run from repository root directory
4. Check file permissions for scripts

### Blueprint Not Working in Home Assistant
1. Verify it passes all validation tests
2. Check Home Assistant logs for specific errors
3. Test with minimal configuration first
4. Validate all referenced entities exist

## Support and Contributing

### Getting Help
- Check existing GitHub Issues for similar problems
- Review Home Assistant blueprint documentation
- Use the community forum for Home Assistant specific questions

### Contributing Improvements
- Submit pull requests for validation improvements
- Report false positives or missed validations
- Suggest new validation checks
- Improve documentation and examples
