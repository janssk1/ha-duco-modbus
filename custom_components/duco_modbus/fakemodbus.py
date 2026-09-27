"""Fake Modbus unit for development and tests."""

from __future__ import annotations


class FakeModbusUnit:
    """In-memory Modbus unit matching the ModbusUnit protocol."""

    INPUT_REGISTERS: dict[int, int] = {
        10: 10,
        11: 0,
        12: 69,
        20: 12,
        21: 0,
        22: 44,
        23: 201,
        24: 3003,
        25: 8001,
        29: 1,
    }

    HOLDING_REGISTERS: dict[int, int] = {
        10: 65535,
    }

    @property
    def connected(self) -> bool:
        """Return connected state."""
        return True

    @staticmethod
    def _read_block(
        address: int, count: int, registers: dict[int, int]
    ) -> list[int]:
        return [registers[address + offset] for offset in range(count)]

    async def read_input_registers(self, address: int, count: int) -> list[int]:
        """Read input registers."""
        return self._read_block(address, count, self.INPUT_REGISTERS)

    async def read_holding_registers(self, address: int, count: int) -> list[int]:
        """Read holding registers."""
        return self._read_block(address, count, self.HOLDING_REGISTERS)

    async def write_register(self, address: int, value: int) -> None:
        """Write a holding register."""
        self.HOLDING_REGISTERS[address] = value

    async def write_registers(self, address: int, values: list[int]) -> None:
        """Write multiple holding registers."""
        for offset, value in enumerate(values):
            self.HOLDING_REGISTERS[address + offset] = value

    async def read_coils(self, address: int, count: int) -> list[bool]:
        """Read coils (not used by Duco)."""
        return [False] * count

    async def read_discrete_inputs(self, address: int, count: int) -> list[bool]:
        """Read discrete inputs (not used by Duco)."""
        return [False] * count

    async def write_coil(self, address: int, value: bool) -> None:
        """Write coil (not used by Duco)."""

    async def write_coils(self, address: int, values: list[bool]) -> None:
        """Write coils (not used by Duco)."""
