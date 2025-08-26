# Daily Weather Report to Telegram Blueprint

## Overview

This comprehensive blueprint provides automated daily weather reports in French via Telegram, featuring detailed meteorological information, weather alerts, camera snapshots, and presence-based execution control. It's designed for French-speaking users who want a comprehensive daily weather briefing with visual context from their security cameras.

## Key Features

- **French-language weather reports** with localized formatting
- **Weather alert integration** with color-coded warnings (Rouge/Orange/Jaune)
- **Multi-camera snapshot attachments** for visual context
- **Presence-based execution** (typically runs when absent)
- **Indoor/outdoor temperature comparison**
- **Configurable scheduling** via `input_datetime`
- **Multi-bot Telegram support** for complex configurations
- **Comprehensive error handling** with continue-on-error logic

## Architecture

### Message Structure

The generated weather report includes:

1. **Greeting**: "Bonjour," (Good morning)
2. **Current conditions**: Outdoor and indoor temperatures
3. **Weather forecast**: Maximum expected temperature
4. **Weather alerts**: Color-coded French meteorological warnings
5. **Timestamp**: Sent date and time
6. **Camera snapshots**: Visual attachments from configured cameras

### Alert System

Supports French météo-vigilance levels:

- 🟥 **Rouge** (Red): Extreme danger
- 🟧 **Orange** (Orange): High danger
- 🟨 **Jaune** (Yellow): Moderate risk
- 🟩 **Vert** (Green): No particular risk

### Execution Logic

```text
Time Trigger → Presence Check → Weather Message → Camera Snapshots → Telegram Delivery
```

## Required Configuration

### Essential Parameters

1. **Time Helper** (`time_helper`)
   - Type: `input_datetime` (time-only)
   - Purpose: Daily execution schedule
   - Format: Time-only configuration for daily repetition

2. **Presence Boolean** (`presence_boolean`)
   - Type: `input_boolean`
   - Purpose: Execution control (typically absence detection)
   - Logic: Automation runs only when boolean is ON

3. **Indoor Temperature** (`indoor_temp`)
   - Type: `sensor` domain entity
   - Purpose: Main room temperature reading
   - Display: Included in weather comparison

4. **Outdoor Temperature** (`outdoor_temp`)
   - Type: `sensor` domain entity
   - Purpose: External temperature reading
   - Display: Primary weather condition

5. **Cameras** (`cameras`)
   - Type: Multiple `camera` domain entities
   - Purpose: Visual context snapshots
   - Processing: Individual snapshots sent sequentially

6. **Chat IDs** (`chat_ids`)
   - Type: Multiple text inputs
   - Format: Telegram chat IDs (numeric)
   - Purpose: Message recipients

### Optional Parameters

7. **Weather Alert Sensor** (`weather_alert_sensor`)
   - Type: `sensor` domain entity
   - Purpose: French météo-vigilance integration
   - Default: Empty (optional feature)

8. **Telegram Config Entry ID** (`telegram_config_entry_id`)
   - Type: Text input
   - Purpose: Specific bot selection (multi-bot environments)
   - Default: Uses default configured bot

## Setup Guide

### Step 1: Create Required Helpers

Create the scheduling helper:

```yaml
input_datetime:
  weather_report_time:
    name: "Weather Report Time"
    has_time: true
    has_date: false
```

Create the presence control:

```yaml
input_boolean:
  absent:
    name: "Absent Mode"
    icon: mdi:home-export-outline
```

### Step 2: Weather Integration

Ensure you have weather sensors configured. Common integrations:

```yaml
# Example: AccuWeather integration
sensor:
  - platform: template
    sensors:
      outdoor_temperature:
        friendly_name: "Outdoor Temperature"
        value_template: "{{ states('weather.accuweather') }}"
        unit_of_measurement: "°C"
```

### Step 3: French Weather Alerts (Optional)

For météo-vigilance integration, configure a sensor that provides French weather warnings:

```yaml
# Example: Météo-France integration
sensor:
  - platform: meteo_france
    # Configuration for French weather alerts
```

### Step 4: Camera Configuration

Ensure cameras are accessible and create snapshots directory:

```bash
mkdir -p /config/www/snapshots
```

Add to configuration.yaml:

```yaml
homeassistant:
  allowlist_external_dirs:
    - /config/www/snapshots
```

### Step 5: Telegram Bot Setup

Configure Telegram bot with French chat recipients:

```yaml
telegram_bot:
  - platform: polling
    api_key: "YOUR_BOT_TOKEN"
    allowed_chat_ids:
      - 123456789      # Personal chat
      - -1001122334455 # Family group
```

## Message Examples

### Standard Weather Report

```text
Bonjour,

Aujourd'hui :

• Température extérieure : 18.5 °C
• Maximum attendu de 24°C
• Température pièce principale : 21.2 °C

Envoyé le 15/12/2024 07:30.
```

### With Weather Alert

```text
Bonjour,

Aujourd'hui :

• Température extérieure : 18.5 °C
• Maximum attendu de 24°C
• Température pièce principale : 21.2 °C

__Attention, alerte météo en cours__ : 🟧 Vent violent (Orange), 🟨 Pluie-inondation (Jaune)

Envoyé le 15/12/2024 07:30.
```

### Sensor Unavailable

```text
Bonjour,

Aujourd'hui :

• Température extérieure : (indisponible)
• Maximum attendu de 24°C
• Température pièce principale : (indisponible)

Envoyé le 15/12/2024 07:30.
```

## Advanced Configuration

### Custom Temperature Sources

#### Heat Index Integration

```yaml
# Use computed heat index instead of raw temperature
indoor_temp: sensor.computed_heat_index
outdoor_temp: sensor.weather_heat_index
```

#### Multi-sensor Average

```yaml
# Template sensor for multiple outdoor sensors
sensor:
  - platform: template
    sensors:
      average_outdoor_temp:
        value_template: >
          {{ ((states('sensor.north_temp')|float +
               states('sensor.south_temp')|float) / 2) | round(1) }}
```

### Alert Customization

#### Custom Alert Mapping

The blueprint automatically processes French météo-vigilance attributes. For custom alert sensors:

```yaml
# Custom alert sensor template
sensor:
  - platform: template
    sensors:
      custom_weather_alert:
        value_template: >
          {% if states('sensor.wind_speed')|float > 50 %}
            Orange
          {% elif states('sensor.wind_speed')|float > 30 %}
            Jaune
          {% else %}
            Vert
          {% endif %}
        attributes:
          Vent: >
            {% if states('sensor.wind_speed')|float > 50 %}
              Orange
            {% elif states('sensor.wind_speed')|float > 30 %}
              Jaune
            {% else %}
              Vert
            {% endif %}
```

### Multi-Camera Strategy

#### Sequential Capture with Delays

The blueprint includes small delays between camera operations to ensure reliable capture:

```yaml
# Built-in delay logic
- delay: "00:00:01"  # Ensures file write completion
```

#### Camera-Specific Captions

Each camera snapshot includes automatically generated captions:

```text
Salon — 15/12/2024 07:30
Jardin — 15/12/2024 07:30
Entrée — 15/12/2024 07:30
```

### Scheduling Variations

#### Weekend vs Weekday

Create multiple automations for different schedules:

```yaml
# Weekday automation: 07:00
# Weekend automation: 09:00
```

#### Seasonal Adjustments

Use template conditions for seasonal scheduling:

```yaml
condition:
  - condition: template
    value_template: >
      {{ now().month in [11, 12, 1, 2] }}  # Winter months
```

## French Localization

### Date Formatting

The blueprint uses French date formatting:

- `%d/%m/%Y %H:%M` format (DD/MM/YYYY HH:MM)
- French text: "Envoyé le" (Sent on)

### Weather Terms

- **Température extérieure**: Outdoor temperature
- **Température pièce principale**: Main room temperature
- **Maximum attendu**: Expected maximum
- **Attention, alerte météo en cours**: Weather alert in progress

### Alert Levels

- **Rouge**: Extreme danger (red)
- **Orange**: High danger (orange)
- **Jaune**: Moderate risk (yellow)
- **Vert**: No particular risk (green)

## Troubleshooting

### Common Issues

1. **Messages not sending**
   - Check presence boolean state (must be ON)
   - Verify Telegram bot configuration
   - Review chat IDs format (numeric only)

2. **Temperature showing as unavailable**
   - Verify sensor entity IDs are correct
   - Check sensor states in Developer Tools
   - Ensure sensors report numeric values

3. **Camera snapshots failing**
   - Verify `/config/www/snapshots/` directory exists
   - Check camera entity accessibility
   - Review Home Assistant logs for camera errors

4. **Weather alerts not appearing**
   - Verify alert sensor configuration
   - Check sensor attributes match expected format
   - Review template logic in Developer Tools

### Debug Information

Monitor these areas for troubleshooting:

- **Automation traces**: Review execution flow
- **System logs**: Check for camera and Telegram errors
- **Sensor states**: Verify temperature and alert sensors
- **File system**: Confirm snapshot file creation

### Testing Components

#### Test Weather Message

```yaml
service: telegram_bot.send_message
data:
  target: [YOUR_CHAT_ID]
  message: |
    Test weather report:
    • Temperature: {{ states('sensor.outdoor_temp') }}°C
    • Alert: {{ states('sensor.weather_alert') }}
```

#### Test Camera Snapshot

```yaml
service: camera.snapshot
data:
  entity_id: camera.test_camera
  filename: /config/www/snapshots/test.jpg
```

## Performance Considerations

### Resource Management

- **Sequential processing**: Cameras processed one by one
- **Error handling**: Continue-on-error prevents cascade failures
- **File cleanup**: Consider periodic snapshot cleanup
- **Network usage**: Multiple large images may impact bandwidth

### Timing Optimization

- **Single mode**: Prevents overlapping executions
- **Presence check**: Avoids unnecessary processing when home
- **Trace storage**: Limited to 20 traces for performance

### Storage Management

- **Snapshot accumulation**: Implement cleanup automation
- **File naming**: Timestamped files prevent conflicts
- **Directory monitoring**: Monitor disk usage

## Integration Examples

### Home Automation Ecosystem

```yaml
# Integration with vacation mode
condition:
  - condition: state
    entity_id: input_boolean.vacation_mode
    state: "on"
```

### Weather-Based Alerts

```yaml
# Additional weather-based automations
trigger:
  - platform: numeric_state
    entity_id: sensor.weather_alert_level
    above: 2  # Orange/Rouge alerts
```

### Smart Home Dashboard

Display current weather status on dashboards using the same sensors.

## Version History

- **v1.0**: Initial French weather report functionality
- **v1.1**: Added météo-vigilance alert integration
- **v1.2**: Enhanced multi-camera support with error handling
- **v1.3**: Improved template efficiency and documentation
- **v1.4**: Added presence-based execution and multi-bot support
