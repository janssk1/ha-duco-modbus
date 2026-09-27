"""The Duco Modbus integration."""

from __future__ import annotations

from dataclasses import dataclass
import logging

from homeassistant.components.modbus import async_get_unit
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady

from .const import CONF_FAKE, CONF_UNIT, DOMAIN
from .coordinator import DucoCoordinator
from .entity import NodeInfo
from .fakemodbus import FakeModbusUnit
from .modbus_model import (
    PARAM_LOCALIZATION_NUMBER,
    PARAM_MODULE_TYPE,
    ModuleType,
)
from .modbus_params import create_modbus_params
from .modbus_util import ModbusUtil

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [
    Platform.SENSOR,
    Platform.NUMBER,
    Platform.SELECT,
]


@dataclass
class DucoRuntimeData:
    """Runtime data stored on the config entry."""

    coordinator: DucoCoordinator
    nodes: list[NodeInfo]


type DucoConfigEntry = ConfigEntry[DucoRuntimeData]


def _get_modbus_util(entry: DucoConfigEntry, hass: HomeAssistant) -> ModbusUtil:
    unit_id = entry.data[CONF_UNIT]
    if entry.data.get(CONF_FAKE):
        _LOGGER.warning("Using fake Modbus unit for Duco Modbus")
        return ModbusUtil(FakeModbusUnit(), unit_id)
    unit = async_get_unit(
        hass, entry, create_modbus_params(entry.data), unit_id
    )
    return ModbusUtil(unit, unit_id)


async def async_setup_entry(hass: HomeAssistant, entry: DucoConfigEntry) -> bool:
    """Set up a config entry."""
    modbus = _get_modbus_util(entry, hass)
    nodes: list[NodeInfo] = []
    coordinator = DucoCoordinator(modbus, hass, entry)
    master = await PARAM_MODULE_TYPE.async_read(modbus, 10)
    if not master:
        raise ConfigEntryNotReady(
            f"Modbus unit {entry.data[CONF_UNIT]} not reachable. Check the logs."
        )

    nodes.append(NodeInfo(coordinator, ModuleType.MASTER_UNIT, 10, None))
    for i in range(2, 7):
        node_id = i * 10
        module_type: ModuleType | None = await PARAM_MODULE_TYPE.async_read(
            modbus, node_id
        )
        if module_type:
            _LOGGER.info("Detected %s", module_type.name)
            location: int = await PARAM_LOCALIZATION_NUMBER.async_read(modbus, node_id)
            nodes.append(NodeInfo(coordinator, module_type, node_id, location))

    await coordinator.async_config_entry_first_refresh()

    entry.runtime_data = DucoRuntimeData(coordinator=coordinator, nodes=nodes)
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    await coordinator.async_refresh()
    return True


async def async_unload_entry(hass: HomeAssistant, entry: DucoConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
