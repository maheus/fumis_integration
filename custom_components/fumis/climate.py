"""Platform for Roth Touchline floor heating controller."""
import logging
import voluptuous as vol

from homeassistant.components.climate import ClimateEntity

from homeassistant.components.climate.const import (
    ATTR_CURRENT_TEMPERATURE,
    HVAC_MODE_OFF,
    HVAC_MODE_HEAT,
    HVAC_MODE_COOL,
    PRESET_NONE,
    PRESET_ECO,
    SUPPORT_PRESET_MODE,
    SUPPORT_TARGET_TEMPERATURE,
    CURRENT_HVAC_OFF,
    CURRENT_HVAC_HEAT,
    CURRENT_HVAC_COOL,
)

from homeassistant.const import (
    ATTR_TEMPERATURE,
    CONF_NAME,
    TEMP_CELSIUS,
)

from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers import entity_platform, config_validation as cv
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.core import HomeAssistant

from .fumis.const import (
    STATUS_OFF,
    STATUS_PRE_HEATING,
    STATUS_IGNITION,
    STATUS_COMBUSTION,
    STATUS_ECO,
    STATUS_COOLING,
    STATUS_UNKNOWN,
)

from .const import (
    DOMAIN,
    MANUFACTURER,
)

_LOGGER = logging.getLogger(__name__)

SUPPORT_FLAGS = SUPPORT_TARGET_TEMPERATURE | SUPPORT_PRESET_MODE
HVAC_MODES = [HVAC_MODE_OFF, HVAC_MODE_HEAT]
PRESET_MODES = [PRESET_NONE, PRESET_ECO]

HA_PRESET_TO_FUMIS = {
    PRESET_NONE: 0,
    PRESET_ECO: 1,
}

FUMIS_PRESET_TO_HA = {
    "off": PRESET_NONE,
    "on": PRESET_ECO,
}

FUMIS_HVAC_TO_HA = {
    STATUS_OFF: HVAC_MODE_OFF,
    STATUS_PRE_HEATING: HVAC_MODE_HEAT,
    STATUS_IGNITION: HVAC_MODE_HEAT,
    STATUS_COMBUSTION: HVAC_MODE_HEAT,
    STATUS_ECO: HVAC_MODE_HEAT,
    STATUS_COOLING: HVAC_MODE_COOL,
    STATUS_UNKNOWN: HVAC_MODE_OFF,
}

FUMIS_CURRENT_HVAC_TO_HA = {
    STATUS_OFF: CURRENT_HVAC_OFF,
    STATUS_PRE_HEATING: CURRENT_HVAC_HEAT,
    STATUS_IGNITION: CURRENT_HVAC_HEAT,
    STATUS_COMBUSTION: CURRENT_HVAC_HEAT,
    STATUS_ECO: CURRENT_HVAC_HEAT,
    STATUS_COOLING: CURRENT_HVAC_COOL,
    STATUS_UNKNOWN: CURRENT_HVAC_OFF,
}

HA_HVAC_TO_FUMIS = {
    HVAC_MODE_OFF: "off",
    HVAC_MODE_HEAT: "on",
}

FUMIS_SET_POWER_STOVE = "set_power_stove"

async def async_setup_entry(
        hass: HomeAssistant,
        entry: ConfigEntry,
        async_add_entities: AddEntitiesCallback,
    ) -> None:
    """Set up a climate from a config entry."""

    fumis    = hass.data[DOMAIN][entry.entry_id]
    name     = entry.data[CONF_NAME]
    platform = entity_platform.async_get_current_platform()

    if fumis is None:
        print('errors')
    else:
        async_add_entities([FumisClimate(fumis, name)], True)
        platform.async_register_entity_service(
            FUMIS_SET_POWER_STOVE,
            {vol.Required("power"): cv.positive_int},
            "set_power_stove",
        )

class FumisClimate(ClimateEntity):
    """Representation of an Fumis sensor."""
    def __init__(self, fumis, name: str):
        self.fumis = fumis
        self._name = name
        self.info = None
        self._unit_id = None
        self._unit_version = None
        self._state = None
        self._status = None
        self._temperature = None
        self._target_temperature = None
        self._ecomode_state = None


    @property
    def name(self):
        """Return the name."""
        return self._name

    @property
    def device_state_attributes(self):
        """Get device state attributes"""
        return {
                ATTR_CURRENT_TEMPERATURE: self._temperature,
                ATTR_TEMPERATURE: self._target_temperature,
            }

    async def async_update(self):
        """Async update."""
        self.info = await self.fumis.update_info()
        self._unit_id = self.info.unit_id
        self._unit_version = self.info.unit_version
        self._state = self.info.state
        self._status = self.info.status
        self._temperature = self.info.temperature
        self._target_temperature = self.info.target_temperature
        self._ecomode_state = self.info.ecomode_state

    @property
    def unique_id(self):
        """Return a unique_id for this entity."""
        return self._unit_id

    @property
    def hvac_mode(self):
        """Return current operation ie. heat, cool, idle."""
        return FUMIS_HVAC_TO_HA[self._status]

    @property
    def hvac_action(self):
        """Return current HVAC operation ie. heating, cooling, idle."""
        return FUMIS_CURRENT_HVAC_TO_HA[self._status]

    @property
    def hvac_modes(self):
        """Return the list of available operation modes."""
        return HVAC_MODES

    async def async_set_hvac_mode(self, hvac_mode):
        """Set HVAC mode."""
        if HA_HVAC_TO_FUMIS[hvac_mode] == 'on':
            await self.fumis.turn_on()

        if HA_HVAC_TO_FUMIS[hvac_mode] == 'off':
            await self.fumis.turn_off()

    @property
    def supported_features(self):
        """Return the list of supported features."""
        return SUPPORT_FLAGS

    @property
    def preset_mode(self):
        """Return the preset_mode."""
        return FUMIS_PRESET_TO_HA[self._ecomode_state]

    async def async_set_preset_mode(self, preset_mode):
        """Set preset mode."""
        await self.fumis.set_mode(HA_PRESET_TO_FUMIS[preset_mode])

    @property
    def preset_modes(self):
        """List of available preset modes."""
        return PRESET_MODES

    @property
    def device_info(self) -> DeviceInfo:
        """Return device information for this sensor."""
        return DeviceInfo(
            identifiers={
                (DOMAIN, self._unit_id)
            },
            name=self._name,
            sw_version=self._unit_version,
            manufacturer=MANUFACTURER,
        )

    @property
    def temperature_unit(self):
        """Return the unit of measurement which this thermostat uses."""
        return TEMP_CELSIUS

    @property
    def current_temperature(self):
        """Return the current temperature."""
        return self._temperature

    @property
    def target_temperature(self):
        """Return the temperature we try to reach."""
        return self._target_temperature

    @property
    def target_temperature_step(self):
        """Return the supported step of target temperature."""
        return 0.1

    async def async_set_temperature(self, **kwargs):
        """Set new target temperature."""
        await self.fumis.set_target_temperature(kwargs.get(ATTR_TEMPERATURE))

    async def async_turn_on(self):
        """Turn device on."""
        await self.fumis.turn_on()

    async def async_turn_off(self):
        """Turn device off."""
        await self.fumis.turn_off()

    async def set_power_stove(self, power) -> None:
        """Set the power value."""
        await self.fumis.set_power(power)
