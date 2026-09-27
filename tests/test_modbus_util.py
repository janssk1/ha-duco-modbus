"""Unit tests for ModbusUtil with FakeModbusUnit."""

import pytest

from homeassistant.components.modbus.const import CALL_TYPE_REGISTER_INPUT

from custom_components.duco_modbus.fakemodbus import FakeModbusUnit
from custom_components.duco_modbus.modbus_util import ModbusUtil


@pytest.mark.asyncio
async def test_read_master_fan_register() -> None:
    """Read ventilation percentage on master node."""
    util = ModbusUtil(FakeModbusUnit(), 1)
    value = await util.read_register(12, CALL_TYPE_REGISTER_INPUT)
    assert value == 69
