"""Data update coordinator for Duco Modbus."""

from __future__ import annotations

from datetime import timedelta
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import DOMAIN
from .modbus_util import ModbusAddressRegistry, ModbusRegisters, ModbusUtil

_LOGGER = logging.getLogger(__name__)


class DucoCoordinator(DataUpdateCoordinator[ModbusRegisters]):
    """Hold polled Modbus register cache for Duco entities."""

    def __init__(
        self, modbus: ModbusUtil, hass: HomeAssistant, config_entry: ConfigEntry
    ) -> None:
        """Initialize."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            config_entry=config_entry,
            update_interval=timedelta(seconds=15),
        )
        self.modbus = modbus
        self.modbus_register_provider = ModbusAddressRegistry()

    async def _async_update_data(self) -> ModbusRegisters:
        return await self.modbus_register_provider.async_read_all_registers(
            self.modbus
        )
