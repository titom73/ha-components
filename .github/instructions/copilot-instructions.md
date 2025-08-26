# Copilot Instructions – Home Assistant Configurations

Ces instructions servent de guide pour générer des fichiers **Home Assistant** valides et optimisés.

## Style YAML

- Sortie **100% YAML Home Assistant valide**.
- **ASCII uniquement**, pas de caractères Unicode.
- Indentation **2 espaces**, pas de tabulations.
- Utiliser `alias`, `id`, `description`, `mode` dans les automations.
- Commenter les blocs clefs avec `#`.
- Messages multi-lignes → blocs `|`.
- Toujours prévoir une valeur par défaut dans les templates Jinja (`|float(0)`, `|int(0)`).

## Organisation des fichiers

- Fichier racine `configuration.yaml` minimal, utiliser `!include` :

```yaml
homeassistant:
  packages: !include_dir_named packages/

automation: !include_dir_merge_list automations/
script: !include_dir_merge_list scripts/
scene: !include_dir_merge_list scenes/
template: !include templates.yaml
```

- Arborescence type :

```
.
├── configuration.yaml
├── templates.yaml
├── packages/
│   ├── energy.yaml
│   └── climate.yaml
├── automations/
│   ├── lights_night.yaml
│   └── alerts.yaml
├── blueprints/
│   ├── Scope1/
│   │   ├── lights_night.yaml
│   │   └── alerts.yaml
├── scripts/
│   └── snapshots.yaml
└── scenes/
    └── evening.yaml
```

## Bonnes pratiques Copilot

- Toujours générer du YAML clair et vérifié.
- Utiliser des entités cohérentes (light.cuisine, input_boolean.matin).
- Favoriser des workflows simples et robustes.
- Préférer !include_dir_merge_list pour listes (automations, scripts, scenes).
- Préférer !include_dir_named pour packages.
- Ajouter des commentaires pour clarifier la logique.
- Les affichages utilisateurs sont en français.
- Le code doit etre en anglais (entités, services, attributs et descriptions).

## Exemples à suivre

### Automation simple

```yaml
alias: Wake - Kitchen at 07:30
id: wake_kitchen_0730
description: Turn on kitchen lights at 07:30 if morning mode is on for 5 minutes
mode: single
triggers:
  - trigger: time
    at: "07:30:00"
conditions:
  - condition: state
    entity_id: input_boolean.matin
    state: "on"
    for: "00:05:00"
actions:
  - service: light.turn_on
    target:
      entity_id: light.cuisine
    data:
      brightness_pct: 60
  - delay: "00:30:00"
  - service: light.turn_off
    target:
      entity_id: light.cuisine
```

### Template sensor

```yaml
template:
  - sensor:
      - name: temperature_moyenne
        unique_id: temperature_moyenne_3_capteurs
        unit_of_measurement: "C"
        state: >
          {% set vals = [
            states('sensor.t1')|float(0),
            states('sensor.t2')|float(0),
            states('sensor.t3')|float(0)
          ] %}
          {{ (vals | sum / (vals | length)) | round(1) }}
```

### Blueprint minimal

```yaml
blueprint:
  name: Light On Schedule
  domain: automation
  source_url: https://example.invalid/blueprint/light_on_schedule
  input:
    target_light:
      name: Light entity
      selector:
        entity:
          domain: light
    time_on:
      name: Time to turn on
      selector:
        time: {}
    duration:
      name: Duration to keep on (HH:MM:SS)
      default: "00:30:00"
      selector:
        text: {}

alias: Light On Schedule
description: Turn on a light at a specific time for a fixed duration
mode: single
triggers:
  - trigger: time
    at: !input time_on
conditions: []
actions:
  - service: light.turn_on
    target:
      entity_id: !input target_light
  - delay: !input duration
  - service: light.turn_off
    target:
      entity_id: !input target_light
```

## Vérification

- Toujours vérifier la config avant redémarrage :
- Interface : Outils de développement > YAML > Vérifier la configuration.
- CLI : hass --script check_config.
- Recharger les domaines (Automations, Scripts, Scenes, Templates) via l’UI quand possible.

## Checklist rapide

- ASCII uniquement.
- Indentation 2 espaces.
- YAML Home Assistant valide.
- Ajout d’alias, id, description, mode.
- Valeurs par défaut dans les templates.
- Favoriser !include et packages.

