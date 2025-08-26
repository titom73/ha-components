# Cover Heat Management Blueprint

## Overview

This advanced automation blueprint provides intelligent cover (shutters/blinds) management based on temperature thresholds with hysteresis, solar filtering, and automatic restoration capabilities. It implements a three-tier temperature system (T1, T2, T3) with progressive protection levels and prevents oscillations through smart state management.

## Key Features

- **Three-tier temperature system** with configurable thresholds (T1 < T2, T3 < T1)
- **Hysteresis control** to prevent rapid switching
- **Solar position filtering** based on azimuth and elevation
- **Automatic scene snapshotting** and restoration before sunset
- **Guard system** to prevent unwanted T3 actions
- **Zone state tracking** to ensure single execution per zone entry
- **Customizable additional actions** for each temperature tier

## Architecture

### Temperature Zones

1. **T1 Zone (Medium Protection)**: Temperature reaches T1 + hysteresis
2. **T2 Zone (Intense Protection)**: Temperature reaches T2 + hysteresis
3. **T3 Zone (Return to Initial)**: Temperature drops below T3 for 10 minutes

### State Management

- **Zone State**: Tracks current temperature zone (none/t1/t2)
- **T3 Guard**: Prevents T3 actions unless T1 or T2 has been applied
- **Snapshot System**: Automatically captures cover positions before first protection

## Required Configuration

### Essential Entities

1. **Temperature Sensor** (`temp_sensor`)
   - Domain: `sensor`
   - Device class: `temperature`
   - Purpose: Primary temperature reading for decisions

2. **Temperature Helpers** (3x `input_number`)
   - `t1_helper`: Medium protection threshold
   - `t2_helper`: Intense protection threshold (must be > T1)
   - `t3_helper`: Return threshold (must be < T1)

3. **Scenes** (2x `scene`)
   - `scene_1`: Applied when reaching T1 zone
   - `scene_2`: Applied when reaching T2 zone

4. **Covers** (`cover`, multiple allowed)
   - Target covers for snapshot/restore and T3 opening

5. **Control Helpers**
   - `t3_guard_helper` (`input_boolean`): Guards T3 actions
   - `zone_state_helper` (`input_select`): Must have exact options: `none`, `t1`, `t2`

### Optional Configuration

#### Hysteresis Settings

- `hys_t1`: Hysteresis around T1 (default: 0.3°C)
- `hys_t2`: Hysteresis around T2 (default: 0.3°C)

#### Solar Filtering

- `sun_filter_enabled`: Enable/disable solar position filtering
- `azimuth_min/max`: Solar azimuth window (0-360°)
- `elevation_min/max`: Solar elevation window (-90 to 90°)

#### Additional Actions

- `on_t1_actions`: Custom actions after Scene 1
- `on_t2_actions`: Custom actions after Scene 2
- `on_t3_actions`: Custom actions after cover opening

## Operational Logic

### Trigger Conditions

1. **State Changes**: Temperature sensor, thresholds, or zone state changes
2. **Temperature Cooldown**: Temperature < T3 for 10 minutes
3. **Solar Changes**: Sun position changes (if solar filter enabled)
4. **Pre-sunset**: 5 minutes before sunset

### Decision Flow

```text
Temperature Reading → Solar Filter Check → Hysteresis Evaluation → Zone State Check → Action Execution
```

### Action Sequences

#### T1 Entry (Medium Protection)

1. Create snapshot (if first protection)
2. Apply Scene 1
3. Arm T3 guard
4. Execute additional T1 actions
5. Set zone state to "t1"

#### T2 Entry (Intense Protection)

1. Create snapshot (if first protection)
2. Apply Scene 2
3. Arm T3 guard
4. Execute additional T2 actions
5. Set zone state to "t2"

#### T3 Cooldown (Return to Initial)

1. Check T3 guard is armed
2. Open all covers
3. Execute additional T3 actions
4. Disarm T3 guard
5. Reset zone state to "none"

#### Pre-sunset Restoration

1. Check if snapshot exists
2. Restore snapshot scene
3. Disarm T3 guard
4. Reset zone state to "none"

## Setup Guide

### Step 1: Create Required Helpers

Create the following helpers in Home Assistant:

```yaml
# input_number helpers
input_number:
  temp_t1_threshold:
    name: "T1 Temperature Threshold"
    min: 15
    max: 35
    step: 0.5
    unit_of_measurement: "°C"

  temp_t2_threshold:
    name: "T2 Temperature Threshold"
    min: 20
    max: 40
    step: 0.5
    unit_of_measurement: "°C"

  temp_t3_threshold:
    name: "T3 Temperature Threshold"
    min: 10
    max: 30
    step: 0.5
    unit_of_measurement: "°C"

# input_boolean helper
input_boolean:
  cover_heat_t3_guard:
    name: "Cover Heat T3 Guard"
    icon: mdi:shield-check

# input_select helper
input_select:
  cover_heat_zone_state:
    name: "Cover Heat Zone State"
    options:
      - "none"
      - "t1"
      - "t2"
    initial: "none"
```

### Step 2: Create Protection Scenes

Create scenes that define your cover positions for each protection level:

```yaml
scene:
  - name: "Covers T1 Protection"
    id: covers_t1_protection
    entities:
      cover.living_room_blinds:
        state: "closed"
        attributes:
          current_position: 70
      cover.bedroom_shutters:
        state: "closed"
        attributes:
          current_position: 60

  - name: "Covers T2 Protection"
    id: covers_t2_protection
    entities:
      cover.living_room_blinds:
        state: "closed"
        attributes:
          current_position: 90
      cover.bedroom_shutters:
        state: "closed"
        attributes:
          current_position: 90
```

### Step 3: Configure Temperature Thresholds

Set appropriate values ensuring: T3 < T1 < T2

Example values:

- T3: 22°C (return to normal)
- T1: 25°C (medium protection)
- T2: 28°C (intense protection)

### Step 4: Configure Solar Filter (Optional)

For south-facing windows (example):

- Azimuth min: 120° (southeast)
- Azimuth max: 240° (southwest)
- Elevation min: 10° (above horizon)
- Elevation max: 70° (high sun)

## Usage

### Daily Operation

Once configured, the blueprint operates automatically based on temperature readings:

1. **Morning/Low Temperature**
   - Covers remain in their normal position
   - Zone state shows "none"
   - T3 guard is disarmed

2. **Temperature Rises to T1**
   - System creates snapshot of current cover positions
   - Applies Scene 1 (medium protection)
   - Arms T3 guard
   - Sets zone state to "t1"

3. **Temperature Continues to T2**
   - Applies Scene 2 (intense protection)
   - Updates zone state to "t2"
   - T3 guard remains armed

4. **Temperature Drops Below T3**
   - After 10 minutes, opens covers automatically
   - Disarms T3 guard
   - Resets zone state to "none"

5. **Evening (5 minutes before sunset)**
   - Restores original cover positions from snapshot
   - Resets all states for next day

### Monitoring and Control

#### Key Entities to Monitor

- **Zone State** (`input_select.zone_state_helper`): Shows current temperature zone
- **T3 Guard** (`input_boolean.t3_guard_helper`): Indicates if T3 actions are enabled
- **Temperature Sensor**: Current temperature reading
- **Scene Snapshots**: Automatically created scenes for restoration

#### Manual Override

You can manually control the system:

- Disable automation temporarily by turning it off
- Manually change zone state to force transitions
- Adjust temperature thresholds in real-time
- Toggle T3 guard to prevent/allow cover opening

### Seasonal Adjustments

#### Summer Configuration

- T1: 26°C (start medium protection)
- T2: 29°C (increase to intense protection)
- T3: 24°C (return to normal)
- Solar filter: Active during peak hours

#### Winter Configuration

- T1: 22°C (gentler protection)
- T2: 25°C (moderate protection)
- T3: 20°C (return threshold)
- Solar filter: Disabled or adjusted for lower sun angles

### Best Practices

1. **Start Conservative**
   - Begin with higher temperature thresholds
   - Gradually adjust based on comfort and energy savings

2. **Monitor First Week**
   - Check automation traces regularly
   - Verify temperature readings are accurate
   - Adjust hysteresis if oscillations occur

3. **Seasonal Reviews**
   - Update thresholds for seasonal temperature changes
   - Adjust solar filter for seasonal sun positions
   - Review scene configurations for different light conditions

## Troubleshooting

### Common Issues

1. **T3 actions not executing**
   - Verify T3 guard is armed (should be ON after T1/T2 activation)
   - Check temperature stays below T3 for full 10 minutes

2. **Rapid switching between zones**
   - Increase hysteresis values
   - Verify temperature sensor stability

3. **Solar filter not working**
   - Check sun.sun entity is available
   - Verify azimuth/elevation ranges are logical

4. **Snapshots not restoring**
   - Ensure covers support position restoration
   - Check snapshot scene creation in Developer Tools

### Debug Information

Monitor these entities for troubleshooting:

- `input_select.cover_heat_zone_state`: Current temperature zone
- `input_boolean.cover_heat_t3_guard`: T3 guard status
- Scene entities: Check if snapshots are created
- Automation traces: Review decision flow in automation traces

## Advanced Customization

### Custom Temperature Calculations

Modify the temperature variables for complex calculations:

```yaml
# Example: Use heat index instead of raw temperature
T: "{{ states('sensor.heat_index') | float(9999) }}"
```

### Complex Solar Filtering

Implement seasonal adjustments or multiple time-based windows in the solar filter logic.

### Integration with Weather

Add weather-based conditions to prevent actions during rain or high winds:

```yaml
# Additional condition example
condition:
  - condition: numeric_state
    entity_id: sensor.wind_speed
    below: 20
```

## Performance Considerations

- **Mode: restart** ensures latest conditions are evaluated
- **Max exceeded: silent** prevents queue overflow
- **10-minute cooldown** prevents excessive T3 triggering
- **Single execution per zone** prevents duplicate actions

## Version History

- **v1.0**: Initial release with basic temperature zones
- **v1.1**: Added solar filtering capabilities
- **v1.2**: Implemented guard system and zone state tracking
- **v1.3**: Added pre-sunset restoration and custom actions
