"""Config flow for Duco Modbus."""

from __future__ import annotations

import logging
from typing import Any

from modbus_connection import ModbusError
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.components.modbus import async_get_temporary_unit
from homeassistant.config_entries import ConfigFlowResult
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.selector import (
    NumberSelector,
    NumberSelectorConfig,
    NumberSelectorMode,
    SerialPortSelector,
)

from .const import CONF_BAUDRATE, CONF_DEVICE, CONF_FAKE, CONF_UNIT, DEFAULT_BAUDRATE, DOMAIN
from .modbus_model import PARAM_MODULE_TYPE
from .modbus_params import create_modbus_params
from .modbus_util import ModbusUtil

_LOGGER = logging.getLogger(__name__)

UNIT_SELECTOR = vol.All(
    NumberSelector(NumberSelectorConfig(min=1, max=247, mode=NumberSelectorMode.BOX)),
    vol.Coerce(int),
)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_DEVICE): SerialPortSelector(),
        vol.Required(CONF_BAUDRATE, default=DEFAULT_BAUDRATE): vol.All(
            NumberSelector(
                NumberSelectorConfig(min=1200, max=115200, mode=NumberSelectorMode.BOX)
            ),
            vol.Coerce(int),
        ),
        vol.Required(CONF_UNIT, default=1): UNIT_SELECTOR,
        vol.Optional(CONF_FAKE): bool,
    }
)


async def _async_validate_connection(hass: HomeAssistant, data: dict[str, Any]) -> str | None:
    """Validate that the Duco box responds on Modbus."""
    if data.get(CONF_FAKE):
        return None
    try:
        async with async_get_temporary_unit(
            hass, create_modbus_params(data), data[CONF_UNIT]
        ) as unit:
            modbus = ModbusUtil(unit, data[CONF_UNIT])
            if not await PARAM_MODULE_TYPE.async_read(modbus, 10):
                return "cannot_connect"
    except (HomeAssistantError, ModbusError):
        _LOGGER.debug("Cannot connect to Duco device", exc_info=True)
        return "cannot_connect"
    except Exception:
        _LOGGER.exception("Unexpected error connecting to Duco device")
        return "unknown"
    return None


class DucoModbusConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Duco Modbus."""

    VERSION = 2

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}
        if user_input is not None:
            error = await _async_validate_connection(self.hass, user_input)
            if error is not None:
                errors["base"] = error
            else:
                await self.async_set_unique_id(
                    f"{user_input[CONF_DEVICE]}_{user_input[CONF_UNIT]}"
                )
                self._abort_if_unique_id_configured()
                return self.async_create_entry(
                    title="Duco Modbus",
                    data=user_input,
                )

        return self.async_show_form(
            step_id="user",
            data_schema=STEP_USER_DATA_SCHEMA,
            errors=errors,
        )
