"""Tests for Duco Modbus setup."""

from homeassistant.core import HomeAssistant

from custom_components.duco_modbus.const import CONF_DEVICE, CONF_FAKE, CONF_UNIT, DOMAIN
from pytest_homeassistant_custom_component.common import MockConfigEntry


async def test_setup_entry_fake(hass: HomeAssistant, enable_custom_integrations) -> None:
    """Test loading the integration with fake Modbus."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        data={
            CONF_DEVICE: "/dev/ttyTEST",
            CONF_UNIT: 1,
            CONF_FAKE: True,
        },
        title="Duco Modbus",
    )
    entry.add_to_hass(hass)

    assert await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()

    assert entry.runtime_data is not None
    assert len(entry.runtime_data.nodes) >= 1

    fan_states = [
        state
        for state in hass.states.async_all("sensor")
        if state.attributes.get("friendly_name", "").endswith("Fan")
        or state.entity_id.endswith("_fan")
    ]
    assert fan_states
    assert fan_states[0].state == "69"
