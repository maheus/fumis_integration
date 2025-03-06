"""Support for the (unofficial) Fumis API."""
import asyncio
from datetime import timedelta
import logging

import voluptuous as vol
import requests

from homeassistant.components.climate.const import PRESET_AWAY, PRESET_HOME
from homeassistant.config_entries import SOURCE_IMPORT, ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.dispatcher import dispatcher_send
from homeassistant.helpers.event import async_track_time_interval
from homeassistant.util import Throttle
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from homeassistant.const import CONF_PASSWORD, CONF_NAME, CONF_MAC, Platform
from .const import DOMAIN
from .fumis import Fumis, FumisConnectionError

_LOGGER = logging.getLogger(__name__)

DOMAIN = 'fumis'

PLATFORMS = [
    Platform.CLIMATE,
    Platform.SENSOR,
    Platform.BINARY_SENSOR,
]

FUMIS_COMPONENTS = ["climate", "sensor", "binary_sensor"]

MIN_TIME_BETWEEN_UPDATES = timedelta(seconds=10)
SCAN_INTERVAL = timedelta(seconds=15)

CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Schema(
            [{
                vol.Optional(CONF_NAME): cv.string,
                vol.Required(CONF_MAC): cv.string,
                vol.Required(CONF_PASSWORD): cv.string,
            }]
        )
    },
    extra=vol.ALLOW_EXTRA,
)


async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the Fumis component."""

    hass.data.setdefault(DOMAIN, {})

    if DOMAIN not in config:
        return True

    _LOGGER.info("start conf fumis with file")
    for conf in config[DOMAIN]:
        hass.async_create_task(
            hass.config_entries.flow.async_init(
                DOMAIN, context={"source": SOURCE_IMPORT}, data=conf,
            )
        )

    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up this integration using UI."""

    _LOGGER.info("set up fumis with ui")
    mac = entry.data[CONF_MAC]
    password = entry.data[CONF_PASSWORD]
    # if CONF_NAME in entry.data:
    #     name = entry.data[CONF_NAME]
    # else:
    #     name = entry.data[CONF_MAC]
    session = async_get_clientsession(hass)

    try:
        fumis = Fumis(
            mac,
            password,
            loop=hass.loop,
            session=session,
        )
    except FumisConnectionError:
        _LOGGER.error("Fumis update failed")
        return False

    hass.data.setdefault(DOMAIN, {}).update({entry.entry_id: fumis})
    await hass.config_entries.async_forward_entry_setups(entry, FUMIS_COMPONENTS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""

    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data.pop(DOMAIN)
    return unload_ok
