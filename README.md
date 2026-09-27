# Duco Modbus (Home Assistant custom integration)

Custom integration for **Duco** ventilation systems over **Modbus RTU** (e.g. Communication Print / USB–RS485). This is **not** the official [Duco](https://www.home-assistant.io/integrations/duco/) integration (Connectivity Board HTTP).

Tested against **Home Assistant 2024.8.x**; should work on newer releases with minor updates.

## Features

- Auto-discovery of master and room nodes (CO₂, humidity, switch modules)
- Sensors: temperature, CO₂, humidity, fan/valve level
- Controls: ventilation mode select, target %, CO₂/RH setpoints, valve flow

## Installation

1. Copy `custom_components/duco_modbus/` to your Home Assistant config directory:

   ```text
   /config/custom_components/duco_modbus/
   ```

2. Add a **Modbus** serial hub to `configuration.yaml` (see [example_configuration.yaml](example_configuration.yaml)).

3. **Restart** Home Assistant.

4. **Settings → Devices & services → Add integration → Duco Modbus**

5. Choose the Modbus **hub name** and **slave/unit ID** (often `1`).

## Deploy from dev machine (rsync)

```bash
rsync -avz --delete \
  ./custom_components/duco_modbus/ \
  homeassistant@<host>:/config/custom_components/duco_modbus/
```

Restart Home Assistant or reload the integration after updating files.

## Hardware notes

- Default serial: **9600 8N1** RTU (adjust in Modbus YAML if your box differs).
- If register addresses are off by one, check Duco **RegOffs** on the unit.

## Development

Ported from a 2023 Home Assistant fork; Modbus I/O uses `ModbusHub.async_pb_call` (HA 2024.8+).
