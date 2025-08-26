# Home Assistant Blueprints Documentation

This directory contains comprehensive documentation for all Home Assistant blueprints included in this repository.

## Available Blueprints

### Climate Management

#### [Cover Heat Management](cover-heat-management.md)
- **File**: `blueprints/climate/cover-heat-management.yml`
- **Purpose**: Advanced temperature-based cover/shutter automation with hysteresis and solar filtering
- **Complexity**: Advanced
- **Features**: 3-tier temperature system, guard mechanisms, automatic restoration

### Notifications

#### [Camera Snapshot to Telegram](camera-snapshot-to-telegram.md)
- **File**: `blueprints/notifications/camera-sanpshot-to-telegram.yml`
- **Purpose**: Daily automated camera snapshot delivery via Telegram
- **Complexity**: Beginner to Intermediate
- **Features**: Scheduled capture, multi-camera support, customizable captions

#### [Daily Weather Report to Telegram](daily-weather-report-to-telegram.md)
- **File**: `blueprints/notifications/daily-weather-report-to-telegram.yml`
- **Purpose**: Comprehensive French weather reports with alerts and camera snapshots
- **Complexity**: Intermediate to Advanced
- **Features**: French localization, weather alerts, presence control, multi-camera integration

## Quick Start Guide

### Prerequisites

1. **Home Assistant** version 2023.1 or later
2. **Telegram Bot** configured for notifications
3. **Required integrations** based on chosen blueprints:
   - Weather integration (for weather reports)
   - Camera entities (for snapshots)
   - Temperature sensors (for climate management)

### Installation Process

1. **Import Blueprint**
   ```yaml
   # Via UI: Configuration → Automations & Scenes → Blueprints → Import Blueprint
   # Via URL: Paste the raw GitHub URL of the desired blueprint
   ```

2. **Create Required Helpers**
   - See individual documentation for specific helper requirements
   - Common helpers: `input_boolean`, `input_number`, `input_select`, `input_datetime`

3. **Configure Automation**
   - Create new automation from imported blueprint
   - Fill in required parameters
   - Test with trace functionality

### Common Helper Examples

```yaml
# Frequently used helpers across blueprints
input_boolean:
  automation_enabled:
    name: "Enable Automation"
    icon: mdi:toggle-switch

input_datetime:
  daily_time:
    name: "Daily Execution Time"
    has_time: true
    has_date: false

input_number:
  temperature_threshold:
    name: "Temperature Threshold"
    min: 15
    max: 35
    step: 0.5
    unit_of_measurement: "°C"

input_select:
  mode_selector:
    name: "Mode Selector"
    options:
      - "none"
      - "active"
      - "inactive"
```

## Configuration Templates

### Telegram Bot Setup

```yaml
# configuration.yaml
telegram_bot:
  - platform: polling
    api_key: !secret telegram_bot_token
    allowed_chat_ids:
      - !secret telegram_chat_id_personal
      - !secret telegram_chat_id_family

# secrets.yaml
telegram_bot_token: "1234567890:ABCdefGHIjklMNOpqrSTUvwxYZ"
telegram_chat_id_personal: 123456789
telegram_chat_id_family: -1001234567890
```

### File Storage Setup

```yaml
# configuration.yaml
homeassistant:
  allowlist_external_dirs:
    - /config/www
    - /config/www/snapshots

# Create directories
mkdir -p /config/www/snapshots
chmod 755 /config/www/snapshots
```

## Blueprint Comparison

| Feature | Cover Heat | Camera Snapshot | Weather Report |
|---------|------------|-----------------|----------------|
| **Complexity** | Advanced | Beginner | Intermediate |
| **Triggers** | Multiple | Time-based | Time-based |
| **Dependencies** | High | Low | Medium |
| **Customization** | Extensive | Moderate | High |
| **Use Cases** | Climate Control | Security | Information |

## Best Practices

### General Guidelines

1. **Test Thoroughly**
   - Use automation traces for debugging
   - Test individual components before full deployment
   - Start with simple configurations

2. **Documentation**
   - Document your specific configurations
   - Note any customizations made
   - Keep track of entity dependencies

3. **Maintenance**
   - Regular backup of configurations
   - Monitor automation performance
   - Update blueprints when available

4. **Security**
   - Secure Telegram bot tokens
   - Limit file access permissions
   - Regular security reviews

### Performance Optimization

1. **Resource Management**
   - Use appropriate execution modes
   - Implement proper delays for external services
   - Monitor system resource usage

2. **Error Handling**
   - Implement fallback mechanisms
   - Use continue-on-error where appropriate
   - Monitor automation failures

3. **Efficiency**
   - Avoid unnecessary executions
   - Use conditions effectively
   - Optimize template calculations

## Troubleshooting

### Common Issues

1. **Blueprint Import Failures**
   - Check Home Assistant version compatibility
   - Verify YAML syntax
   - Review error logs

2. **Automation Not Triggering**
   - Verify trigger conditions
   - Check entity states
   - Review automation traces

3. **Service Call Failures**
   - Verify entity availability
   - Check service parameters
   - Review integration status

### Debug Tools

1. **Developer Tools**
   - Services: Test individual service calls
   - States: Monitor entity states
   - Events: Track system events

2. **Automation Traces**
   - Review execution flow
   - Identify failure points
   - Monitor performance

3. **System Logs**
   - Check for error messages
   - Monitor warnings
   - Review integration status

## Contributing

### Documentation Standards

- Follow existing documentation structure
- Include practical examples
- Provide troubleshooting information
- Use clear, concise language

### Code Standards

- Follow Home Assistant YAML conventions
- Include comprehensive input validation
- Implement proper error handling
- Document template logic

### Testing

- Test with various configurations
- Verify cross-platform compatibility
- Validate error conditions
- Performance testing

## Support

### Resources

- **Home Assistant Community**: [community.home-assistant.io](https://community.home-assistant.io)
- **Blueprint Exchange**: [blueprints.home-assistant.io](https://blueprints.home-assistant.io)
- **Documentation**: [home-assistant.io/docs](https://home-assistant.io/docs)

### Getting Help

1. **Check Documentation**: Review relevant blueprint documentation
2. **Search Community**: Look for similar issues in the community
3. **Provide Details**: Include configuration and error messages
4. **Test Components**: Isolate issues to specific components

## Version Information

- **Documentation Version**: 1.0
- **Last Updated**: December 2024
- **Compatibility**: Home Assistant 2023.1+
- **Language**: English (with French localization support)
