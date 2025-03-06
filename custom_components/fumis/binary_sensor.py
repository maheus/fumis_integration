"""Platform for Fumis state controller."""
import logging

from homeassistant.const import (
    CONF_NAME,
    CONF_DEVICE_CLASS,
    CONF_ICON,
    CONF_UNIT_OF_MEASUREMENT,
    CONF_TYPE,
)

from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.core import HomeAssistant

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
)

from .const import (
    DOMAIN,
    ATTR_STATUS,
)

_LOGGER = logging.getLogger(__name__)

SENSOR_TYPES = {
    ATTR_STATUS: {
        CONF_NAME: "Stove Status",
        CONF_TYPE: ATTR_STATUS,
        CONF_DEVICE_CLASS: BinarySensorDeviceClass.RUNNING,
    },
}

async def async_setup_entry(
        hass: HomeAssistant,
        entry: ConfigEntry,
        async_add_entities: AddEntitiesCallback,
    ) -> None:
    """Set up sensors from a config entry."""
    fumis = hass.data[DOMAIN][entry.entry_id]
    name = entry.data[CONF_NAME]

    sensors = [
              ATTR_STATUS,
              ]

    if fumis is None:
        print('errors')
    else:
        async_add_entities([FumisBinarySensor(fumis, sensor, name) for sensor in sensors], True)

class FumisBinarySensor(Entity):
    """Representation of a Sensor."""

    def __init__(self, fumis, sensor: str, name: str) -> None:
        self.fumis = fumis
        self._name = name
        self._sensor = SENSOR_TYPES[sensor]
        self.info = None
        self._unit_id = None
        self._state = None

    @property
    def unique_id(self):
        """Return a unique ID."""
        return f"{self._unit_id}-{self._sensor.get(CONF_TYPE)}"

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{self._name} {self._sensor.get(CONF_NAME)}"

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def device_class(self):
        """Return the class of this device."""
        return self._sensor.get(CONF_DEVICE_CLASS)

    @property
    def icon(self):
        """Return the icon of this device."""
        return self._sensor.get(CONF_ICON)

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return self._sensor.get(CONF_UNIT_OF_MEASUREMENT)

    async def async_update(self):
        """Async update."""
        self.info = await self.fumis.update_info()
        self._unit_id = self.info.unit_id
        self._state = getattr(self.info, self._sensor.get(CONF_TYPE))
        _LOGGER.debug("""Export binary sensor info for %s.
                      name: %s value: %s""",
                     self._name, self._sensor.get(CONF_NAME), self._state)

    @property
    def device_info(self) -> DeviceInfo:
        """Return device information for this binary sensor."""
        return DeviceInfo(
            identifiers={
                (DOMAIN, self._unit_id)
            },
            name=self._name,
        )
