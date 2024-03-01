"""Platform for Fumis sensor controller."""
import logging

from homeassistant.const import (
    ATTR_TEMPERATURE,
    ATTR_STATE,
    PERCENTAGE,
    CONF_NAME,
    CONF_DEVICE_CLASS,
    CONF_ICON,
    CONF_UNIT_OF_MEASUREMENT,
    CONF_TYPE,
    UnitOfPower,
    UnitOfTemperature
)

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)

from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.core import HomeAssistant

from .const import (
    DOMAIN,
    ATTR_POWER,
    ATTR_FUEL,
    ATTR_ACTUAL_POWER,
)

_LOGGER = logging.getLogger(__name__)

SENSOR_TYPES = {
    ATTR_TEMPERATURE: {
        CONF_NAME: "Inside Temperature",
        CONF_TYPE: ATTR_TEMPERATURE,
        CONF_DEVICE_CLASS: SensorDeviceClass.TEMPERATURE,
        CONF_UNIT_OF_MEASUREMENT: UnitOfTemperature.CELSIUS,
    },
    ATTR_POWER: {
        CONF_NAME: "Power",
        CONF_TYPE: ATTR_POWER,
        CONF_DEVICE_CLASS: SensorDeviceClass.POWER,
        CONF_UNIT_OF_MEASUREMENT: UnitOfPower.KILO_WATT,
    },
    ATTR_ACTUAL_POWER: {
        CONF_NAME: "Actual Power",
        CONF_TYPE: ATTR_ACTUAL_POWER,
        CONF_DEVICE_CLASS: SensorDeviceClass.POWER,
        CONF_UNIT_OF_MEASUREMENT: UnitOfPower.KILO_WATT,
    },
    ATTR_FUEL: {
        CONF_NAME: "Pellet Quantity",
        CONF_TYPE: ATTR_FUEL,
        CONF_DEVICE_CLASS: SensorDeviceClass.BATTERY,
        CONF_UNIT_OF_MEASUREMENT: PERCENTAGE,
    },
    ATTR_STATE: {
        CONF_NAME: "Current State",
        CONF_TYPE: ATTR_STATE,
        CONF_DEVICE_CLASS: SensorDeviceClass.ENUM,
        CONF_UNIT_OF_MEASUREMENT: None,
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
              ATTR_TEMPERATURE,
              ATTR_POWER,
              ATTR_ACTUAL_POWER,
              ATTR_FUEL,
              ATTR_STATE,
              ]

    async_add_entities([FumisSensor(fumis, sensor, name) for sensor in sensors], True)

class FumisSensor(Entity):
    """Representation of a Sensor."""

    def __init__(self, fumis, sensor: str, name: str) -> None:
        self.fumis = fumis
        self._name = name
        self._sensor = SENSOR_TYPES[sensor]
        self._state = None
        self.info = None
        self._unit_id = None

    @property
    def unique_id(self):
        """Return a unique ID."""
        return f"{self._unit_id}-{self._sensor.get(CONF_TYPE)}"

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{self._name} {self._sensor.get(CONF_NAME)}"

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

    @property
    def native_value(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    async def async_update(self):
        """Async update."""
        self.info = await self.fumis.update_info()
        self._unit_id = self.info.unit_id
        self._state = getattr(self.info, self._sensor.get(CONF_TYPE))
        _LOGGER.debug(f"Export sensor info for {self._name}. name: {self._sensor.get(CONF_NAME)} value: {self._state}")

    @property
    def device_info(self) -> DeviceInfo:
        """Return device information for this sensor."""
        return DeviceInfo(
            identifiers={
                (DOMAIN, self._unit_id)
            },
            name=self._name,
        )
