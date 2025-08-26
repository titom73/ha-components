# Camera Snapshot to Telegram Blueprint

## Overview

This blueprint provides automated daily camera snapshot capture and delivery via Telegram. It's designed for regular surveillance monitoring, vacation security, or daily documentation needs. The automation runs at a scheduled time, captures images from specified cameras, and sends them to configured Telegram recipients with customizable captions.

## Key Features

- **Daily scheduled execution** via `input_datetime` configuration
- **Conditional activation** through `input_boolean` control
- **Multi-camera support** with individual snapshot handling
- **Automatic file management** with organized storage in `/config/www/snapshots/`
- **Customizable captions** with Jinja2 template support
- **Multi-bot support** for complex Telegram configurations
- **Error handling** for robust operation

## Architecture

### Execution Flow

1. **Time Trigger**: Automation activates at the configured time
2. **Condition Check**: Verifies the enable boolean is ON
3. **Snapshot Capture**: Takes snapshot from specified camera
4. **File Storage**: Saves with timestamp and camera name
5. **Telegram Delivery**: Sends photo with caption to all targets

### File Organization

Snapshots are stored as:
```text
/config/www/snapshots/<camera_entity_name>_<YYYYMMDD-HHMMSS>.jpg
```

Example: `living_room_cam_20241201-073000.jpg`

## Required Configuration

### Essential Parameters

1. **Enable Boolean** (`enable_boolean`)
   - Type: `input_boolean`
   - Purpose: Master switch to enable/disable the automation
   - Use case: Vacation mode, maintenance periods

2. **Camera Entity** (`camera_entity`)
   - Type: `camera` domain entity
   - Purpose: Source camera for snapshot capture
   - Requirements: Must support snapshot service

3. **Send Time Entity** (`send_time_entity`)
   - Type: `input_datetime` with time enabled
   - Purpose: Daily execution schedule
   - Supports: Time-only or date+time configurations

4. **Telegram Targets** (`telegram_targets`)
   - Type: Text input (comma-separated)
   - Format: `123456789, -1001122334455`
   - Purpose: List of Telegram chat IDs for delivery

### Optional Parameters

5. **Telegram Config Entry ID** (`telegram_config_entry_id`)
   - Type: Text input
   - Purpose: Specify particular Telegram bot (for multi-bot setups)
   - Default: Uses default configured bot

6. **Caption Template** (`caption_template`)
   - Type: Jinja2 template
   - Default: `{{ state_attr(camera_entity, 'friendly_name') or camera_entity }} — {{ now().strftime('%d/%m/%Y %H:%M') }}`
   - Purpose: Customizable message caption

## Setup Guide

### Step 1: Create Required Helpers

Create an input helper for enabling/disabling the automation:

```yaml
input_boolean:
  daily_camera_snapshot:
    name: "Daily Camera Snapshot"
    icon: mdi:camera-timer
```

Create a time helper for scheduling:

```yaml
input_datetime:
  snapshot_time:
    name: "Daily Snapshot Time"
    has_time: true
    has_date: false
```

### Step 2: Configure File Storage

Ensure `/config/www` is accessible and add to configuration.yaml:

```yaml
homeassistant:
  allowlist_external_dirs:
    - /config/www
    - /config/www/snapshots
```

Create the snapshots directory:

```bash
mkdir -p /config/www/snapshots
```

### Step 3: Telegram Bot Setup

Configure your Telegram bot in Home Assistant:

```yaml
# configuration.yaml
telegram_bot:
  - platform: polling
    api_key: "YOUR_BOT_TOKEN"
    allowed_chat_ids:
      - 123456789      # Your user ID
      - -1001122334455 # Group chat ID
```

### Step 4: Blueprint Configuration

1. Import the blueprint into Home Assistant
2. Create a new automation from the blueprint
3. Configure required parameters:
   - Select your camera entity
   - Choose the enable boolean
   - Set the time helper
   - Enter Telegram chat IDs

## Usage Examples

### Basic Daily Monitoring

**Configuration:**
- Camera: `camera.front_door`
- Time: 08:00 daily
- Enable: `input_boolean.daily_camera_snapshot`
- Targets: Your personal chat ID

**Use case:** Daily front door monitoring for package deliveries

### Vacation Security

**Configuration:**
- Camera: `camera.living_room`
- Time: 12:00 daily
- Enable: `input_boolean.vacation_mode`
- Targets: Family group chat

**Use case:** Security monitoring during vacations

### Multi-location Monitoring

Create multiple automations for different cameras:
- Kitchen: 07:00
- Garden: 12:00
- Garage: 18:00

## Advanced Configuration

### Custom Caption Templates

#### Weather Integration

```jinja2
{{ state_attr(camera_entity, 'friendly_name') }} — {{ now().strftime('%d/%m/%Y %H:%M') }}
Weather: {{ states('weather.home') }} {{ states('sensor.outdoor_temperature') }}°C
```

#### Motion Detection Status

```jinja2
📸 {{ state_attr(camera_entity, 'friendly_name') }}
🕐 {{ now().strftime('%d/%m/%Y %H:%M') }}
🎯 Motion: {{ states('binary_sensor.front_door_motion') | title }}
```

#### Home Occupancy

```jinja2
🏠 {{ state_attr(camera_entity, 'friendly_name') }} — {{ now().strftime('%d/%m/%Y %H:%M') }}
👥 Home: {{ expand('group.family') | selectattr('state', 'eq', 'home') | list | count }} people
```

### Multiple Camera Workflow

For monitoring multiple cameras, create separate automations or use a more complex template:

```yaml
# Multiple automation approach (recommended)
- Front Door Camera: 08:00
- Back Yard Camera: 08:05
- Garage Camera: 08:10
```

### Conditional Execution

Enhance the automation with additional conditions:

```yaml
# Example: Only send during absence
condition:
  - condition: state
    entity_id: input_boolean.daily_camera_snapshot
    state: "on"
  - condition: state
    entity_id: zone.home
    state: "0"  # Nobody home
```

## Troubleshooting

### Common Issues

1. **Snapshots not saved**
   - Check `/config/www/snapshots/` directory exists
   - Verify `allowlist_external_dirs` configuration
   - Ensure camera supports snapshot service

2. **Telegram messages not sent**
   - Verify bot token and chat IDs
   - Check Telegram integration status
   - Test with Developer Tools > Services

3. **Automation not triggering**
   - Verify `input_datetime` is properly configured
   - Check enable boolean state
   - Review automation traces

4. **File permission errors**
   - Ensure Home Assistant has write access to `/config/www/`
   - Check directory ownership and permissions

### Debug Steps

1. **Test Camera Snapshot**
   ```yaml
   service: camera.snapshot
   target:
     entity_id: camera.your_camera
   data:
     filename: /config/www/test_snapshot.jpg
   ```

2. **Test Telegram Delivery**
   ```yaml
   service: telegram_bot.send_photo
   data:
     file: /config/www/test_snapshot.jpg
     caption: "Test message"
     target: [YOUR_CHAT_ID]
   ```

3. **Monitor Automation**
   - Check automation traces
   - Monitor system logs for errors
   - Verify entity states

## Performance Considerations

### File Management

- **Automatic cleanup**: Consider implementing periodic cleanup of old snapshots
- **Storage monitoring**: Monitor `/config/www/snapshots/` disk usage
- **File naming**: Timestamp naming prevents conflicts

### Network Optimization

- **Image quality**: Balance file size vs. quality for faster uploads
- **Retry logic**: Telegram integration includes automatic retry
- **Rate limiting**: Single execution mode prevents overlap

### Resource Usage

- **Camera load**: Stagger multiple camera snapshots
- **Processing time**: Single mode ensures completion before next run
- **Memory usage**: Large images may impact system performance

## Security Considerations

### File Access

- **Web exposure**: Files in `/config/www/` are web-accessible
- **Path traversal**: Validated file naming prevents security issues
- **Cleanup**: Regular cleanup prevents accumulation

### Telegram Security

- **Bot tokens**: Keep bot tokens secure
- **Chat IDs**: Verify recipient chat IDs
- **Message content**: Be mindful of sensitive areas in snapshots

## Integration Examples

### Home Security System

```yaml
# Triggered by security events
alias: "Security Snapshot Alert"
trigger:
  - platform: state
    entity_id: binary_sensor.door_contact
    to: "on"
action:
  - service: camera.snapshot
    # ... snapshot logic
  - service: telegram_bot.send_photo
    # ... immediate alert
```

### Smart Doorbell Integration

```yaml
# Enhanced doorbell with snapshot
trigger:
  - platform: state
    entity_id: binary_sensor.doorbell_button
    to: "on"
```

### Weather-Based Monitoring

```yaml
# Conditional on weather conditions
condition:
  - condition: state
    entity_id: weather.home
    state: "sunny"
```

## Version History

- **v1.0**: Initial release with basic functionality
- **v1.1**: Added multi-bot support and improved error handling
- **v1.2**: Enhanced caption templates and file organization
- **v1.3**: Improved documentation and troubleshooting guides
