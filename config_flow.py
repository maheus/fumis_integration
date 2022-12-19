from homeassistant import data_entry_flow, config_entries
import logging
import voluptuous as vol
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from homeassistant.const import (
    CONF_PASSWORD,
    CONF_NAME,
    CONF_MAC,
    CONF_NAME,
)

from .const import (
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)



#@config_entries.HANDLERS.register(DOMAIN)
class FumisConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):

    async def async_step_user(self, user_input=None):
        _LOGGER.info("start fumis")
        errors = {}
        if user_input is not None:
            mac = user_input[CONF_MAC]
            password = user_input[CONF_PASSWORD]
            name =  user_input[CONF_NAME]
            await self.async_set_unique_id(mac)
            self._abort_if_unique_id_configured()

            return self.async_create_entry(
                title=name, data={CONF_MAC: mac, CONF_PASSWORD: password, CONF_NAME: name},
            )

        # Specify items in the order they are to be displayed in the UI
        data_schema = {
            vol.Optional(CONF_NAME): str,
            vol.Required(CONF_MAC): str,
            vol.Required(CONF_PASSWORD): str,
        }

        return self.async_show_form(
            step_id="user", data_schema=vol.Schema(data_schema), errors=errors
        )

    async def async_step_import(self, user_input=None):
        """Import a config entry.

        """
        self.mac = user_input[CONF_MAC]
        self.password = user_input[CONF_PASSWORD]
        if not self.mac or not self.password:
            return await self.async_step_user(user_input)

        await self.async_set_unique_id(mac)
        self._abort_if_unique_id_configured()

        if CONF_NAME in user_input:
            self.name = user_input[CONF_NAME]

        return self.async_create_entry(
            title=name, data={CONF_MAC: mac, CONF_PASSWORD: password, CONF_NAME: name},
        )
