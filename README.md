# Duco Modbus (Home Assistant custom integration)

Custom integration for **Duco** ventilation systems over **Modbus RTU** (e.g. Communication Print / USB–RS485). This is **not** the official [Duco](https://www.home-assistant.io/integrations/duco/) integration (Connectivity Board HTTP).

Targets **Home Assistant 2026.x** (Modbus via `async_get_unit` / `modbus_connection`). No Modbus block in `configuration.yaml` is required.

## Features

- UI setup: serial port, baud rate, Modbus unit ID
- Auto-discovery of master and room nodes (CO₂, humidity, switch modules)
- Sensors, numbers, and selects for ventilation control and setpoints

## Installation

1. Copy `custom_components/duco_modbus/` to `/config/custom_components/duco_modbus/`.
2. **Restart** Home Assistant.
3. **Settings → Devices & services → Add integration → Duco Modbus**
4. Select the USB serial device (e.g. `/dev/ttyUSB0`), baud rate (default **9600**), and unit ID (often **1**).

Optional debug logging in `configuration.yaml`:

```yaml
logger:
  default: info
  logs:
    custom_components.duco_modbus: debug
```

## Deploy from dev machine

```bash
rsync -avz --delete \
  ./custom_components/duco_modbus/ \
  homeassistant@<host>:/config/custom_components/duco_modbus/
```

## Development / tests

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements_test.txt
pytest tests/
```

Uses [pytest-homeassistant-custom-component](https://github.com/MatthewFlamm/pytest-homeassistant-custom-component) pinned to the same Home Assistant version as your production Pi.

## Hardware notes

- Default serial: **9600 8N1** RTU.
- If register addresses are off by one, check Duco **RegOffs** on the unit.

## Upgrading from 0.1.x

Config flow **version 2** uses serial settings in the integration entry instead of a YAML Modbus hub. Remove any `modbus:` Duco hub from `configuration.yaml`, delete the old integration, and add **Duco Modbus** again.
