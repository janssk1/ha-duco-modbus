"""Constants for the Duco Modbus integration."""

from homeassistant.const import UnitOfRatio

DOMAIN = "duco_modbus"

CONF_DEVICE = "device"
CONF_BAUDRATE = "baudrate"
CONF_UNIT = "unit"
CONF_FAKE = "fake"

DEFAULT_BAUDRATE = 9600

MODEL_NAME = "DucoBox Focus"

CO2_UNIT = UnitOfRatio.PARTS_PER_MILLION
