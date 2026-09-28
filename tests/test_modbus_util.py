"""Unit tests for ModbusUtil with FakeModbusUnit."""

from unittest.mock import AsyncMock, MagicMock

import pytest
from modbus_connection.exceptions import ModbusExceptionError

from homeassistant.components.modbus.const import CALL_TYPE_REGISTER_INPUT

from custom_components.duco_modbus.fakemodbus import FakeModbusUnit
from custom_components.duco_modbus.modbus_util import ModbusUtil


@pytest.mark.asyncio
async def test_read_master_fan_register() -> None:
    """Read ventilation percentage on master node."""
    util = ModbusUtil(FakeModbusUnit(), 1)
    value = await util.read_register(12, CALL_TYPE_REGISTER_INPUT)
    assert value == 69


@pytest.mark.asyncio
async def test_read_registers_returns_none_on_modbus_exception() -> None:
    """Failed reads do not raise (legacy ModbusHub returned no registers)."""
    unit = MagicMock()
    unit.read_input_registers = AsyncMock(
        side_effect=ModbusExceptionError("Modbus Exception 0x04")
    )
    util = ModbusUtil(unit, 1)
    result = await util.read_registers(41, 3, CALL_TYPE_REGISTER_INPUT)
    assert result is None
