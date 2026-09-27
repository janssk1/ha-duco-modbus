"""Build Modbus connection parameters for Duco serial RTU."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from modbus_connection import ModbusSerialParams

from .const import CONF_BAUDRATE, CONF_DEVICE, DEFAULT_BAUDRATE


def create_modbus_params(data: Mapping[str, Any]) -> ModbusSerialParams:
    """Create Modbus serial parameters from config entry data."""
    return ModbusSerialParams(
        device=data[CONF_DEVICE],
        baudrate=data.get(CONF_BAUDRATE, DEFAULT_BAUDRATE),
        bytesize=8,
        parity="N",
        stopbits=1,
    )
