# Home Assistant Components

This repository contains a collection of components and blueprints for Home Assistant, organized by categories to facilitate reuse and maintenance.

## 📁 Repository Structure

### 🏠 Blueprints

Home Assistant blueprints allow you to easily create reusable automations with configurable parameters.

#### Climate / Climate Management

- **`blueprints/climate/cover-heat-management.yml`**
  - **Purpose** : Advanced temperature-based cover management automation
  - **Features** :
    - Temperature tier management (T1, T2, T3) with hysteresis
    - Solar filter to avoid unnecessary actions
    - Progressive protection actions (medium → intense)
    - Automatic restoration before sunset
    - Guard system to prevent oscillations
    - Zone-based state management
  - **Use case** : Automatic solar protection for rooms with motorized covers

#### Notifications

- **`blueprints/notifications/camera-sanpshot-to-telegram.yml`**
  - **Purpose** : Daily camera snapshot sending via Telegram
  - **Features** :
    - Scheduling via `input_datetime`
    - Conditional activation via `input_boolean`
    - Snapshot saving in `/config/www/snapshots/`
    - Multi-camera support
    - Customizable caption templates
  - **Use case** : Automated daily surveillance

- **`blueprints/notifications/daily-weather-report-to-telegram.yml`**
  - **Purpose** : Daily weather report in French via Telegram
  - **Features** :
    - Weather messages in French with alerts
    - Attached camera snapshots
    - Presence/absence management
    - Indoor and outdoor temperatures
    - Weather alert support
    - Scheduling via `input_datetime`
  - **Use case** : Automated daily weather bulletin with visual context

### 📋 Documentation and Guides

#### GitHub Instructions

- **`.github/instructions/markdown-instructions.md`**
  - **Purpose** : Documentation standards and content creation
  - **Content** : Markdown formatting rules, MKdocs structure, best practices

- **`.github/instructions/copilot-instructions.md`**
  - **Purpose** : Guide for generating Home Assistant configurations
  - **Content** : YAML style, file organization, best practices

#### Blueprint Documentation

- **`docs/`**
  - **Purpose** : Comprehensive documentation for all blueprints
  - **Content** : Detailed setup guides, troubleshooting, and usage examples
  - **Access** : [View Documentation](docs/README.md)

## 🚀 Installation and Usage

### Prerequisites

- Home Assistant (recent version recommended)
- Access to blueprints via web interface
- For Telegram notifications: configured Telegram bot

### Blueprint Installation

1. **Via Home Assistant interface** :
   - Go to `Configuration` → `Automations & Scenes` → `Blueprints`
   - Click `Import Blueprint`
   - Paste the URL of the desired blueprint file

2. **Via files** :
   - Copy the `.yml` files to the `blueprints/` folder in your Home Assistant configuration
   - Restart Home Assistant

### Configuration

Each blueprint contains configurable parameters accessible through the graphical interface:

- **Sensors** : Selection of temperature entities, cameras, etc.
- **Thresholds** : Temperature and timing configuration
- **Actions** : Definition of scenes and services to execute
- **Notifications** : Configuration of recipients and messages

## 🔧 Customization

The blueprints are designed to be flexible:

- **Jinja2 Templates** : Message and condition customization
- **Adjustable Parameters** : Thresholds, timings, entities
- **Modular Actions** : Easy replacement of scenes and services

## 🧪 Testing and Validation

This repository includes automated validation to ensure blueprint quality:

- **YAML Syntax Validation** : Ensures all files are properly formatted
- **Blueprint Schema Compliance** : Validates Home Assistant requirements
- **Import Testing** : Simulates loading blueprints into Home Assistant
- **Documentation Sync** : Ensures all blueprints are documented

### Local Testing

```bash
# Run all validation tests
./test-blueprints.sh

# Individual tests
yamllint blueprints/
python3 .github/scripts/validate_blueprint_schema.py
```

### GitHub Actions

Automated testing runs on every push and pull request:
- Basic validation for quick feedback
- Full validation including security scanning
- Documentation synchronization checks

See [Validation Documentation](.github/README.md) for detailed information.

## 📝 Contributing

To contribute to this repository:

1. Follow the guides in `.github/instructions/`
2. Respect Home Assistant YAML conventions
3. Document new components
4. Test blueprints before submission

## 📄 License

This project is distributed under free license for personal and community use.
