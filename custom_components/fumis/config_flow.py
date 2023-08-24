"""Config flow to configure fumis."""
import logging
from homeassistant import config_entries
import voluptuous as vol

from homeassistant.const import (
    CONF_PASSWORD,
    CONF_NAME,
    CONF_MAC,
)

from .const import (
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)


#@config_entries.HANDLERS.register(DOMAIN)
class FumisConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """fumis config flow."""

    def __init__(self) -> None:
        """Initialize the fumis flow."""
        self.mac = None
        self.password = None
        self.name = None

    async def async_step_user(self, user_input=None):
        """Handle a flow initiated by the user."""
        _LOGGER.info("start fumis")
        errors = {}
        if user_input is not None:
            self.mac = user_input[CONF_MAC].upper()
            self.password = user_input[CONF_PASSWORD]
            self.name =  user_input[CONF_NAME]
            await self.async_set_unique_id(self.mac)
            self._abort_if_unique_id_configured()

            return self.async_create_entry(
                title=self.name, data={
                    CONF_MAC: self.mac,
                    CONF_PASSWORD: self.password,
                    CONF_NAME: self.name},
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
        self.mac = user_input[CONF_MAC].upper()
        self.password = user_input[CONF_PASSWORD]
        if not self.mac or not self.password:
            return await self.async_step_user(user_input)

        await self.async_set_unique_id(self.mac)
        self._abort_if_unique_id_configured()

        if CONF_NAME in user_input:
            self.name = user_input[CONF_NAME]

        return self.async_create_entry(
            title=self.name,data={
                CONF_MAC: self.mac,
                CONF_PASSWORD: self.password,
                CONF_NAME: self.name},
        )
