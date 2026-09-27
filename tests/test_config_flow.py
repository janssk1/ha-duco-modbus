"""Tests for Duco Modbus config flow."""

from unittest.mock import patch

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResultType

from custom_components.duco_modbus.const import CONF_DEVICE, CONF_FAKE, CONF_UNIT, DOMAIN


async def test_config_flow_fake(hass: HomeAssistant, enable_custom_integrations) -> None:
    """Test creating an entry with fake Modbus (no hardware)."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result["type"] == FlowResultType.FORM
    assert result["step_id"] == "user"

    with patch(
        "custom_components.duco_modbus.config_flow._async_validate_connection",
        return_value=None,
    ):
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                CONF_DEVICE: "/dev/ttyTEST",
                CONF_UNIT: 1,
                CONF_FAKE: True,
            },
        )

    assert result["type"] == FlowResultType.CREATE_ENTRY
    assert result["title"] == "Duco Modbus"
    assert result["data"][CONF_FAKE] is True
