"""Config flow for Zeversolar integration."""
import logging
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.aiohttp_client import async_get_clientsession
import homeassistant.helpers.config_validation as cv
import requests

from .const import (
    DOMAIN,
    CONF_URL,
    DEFAULT_URL,
    DEFAULT_NAME,
)

_LOGGER = logging.getLogger(__name__)


async def validate_input(hass: HomeAssistant, data):
    """Validate the user input allows us to connect."""
    url = data[CONF_URL]

    # Validate that we can connect to the Zeversolar device
    try:
        response = await hass.async_add_executor_job(
            lambda: requests.get(f"{url}/home.cgi", timeout=10)
        )
        response.raise_for_status()
        
        # Check if the response contains expected data
        data = response.text.strip().split("\n")
        if len(data) < 9:
            return {"error": "invalid_data", "warning": "Invalid data received from Zeversolar device"}
            
        return {"title": DEFAULT_NAME}
    except requests.RequestException as error:
        _LOGGER.warning("Error connecting to Zeversolar: %s", error)
        # Return a warning but allow setup to continue
        return {
            "title": DEFAULT_NAME,
            "warning": f"Could not connect to Zeversolar: {error}. The integration will be added but may not work until the device is online."
        }


class ZeversolarConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Zeversolar."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}
        warning = None

        if user_input is not None:
            info = await validate_input(self.hass, user_input)
            if "error" not in info:
                # If there's a warning, show it but continue with setup
                if "warning" in info:
                    warning = info["warning"]
                
                return self.async_create_entry(title=info["title"], data=user_input)
            
            errors["base"] = info["error"]
            if "warning" in info:
                warning = info["warning"]

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_URL, default=DEFAULT_URL): str,
                }
            ),
            errors=errors,
            description_placeholders={"warning": warning} if warning else None,
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Get the options flow for this handler."""
        return ZeversolarOptionsFlowHandler(config_entry)


class ZeversolarOptionsFlowHandler(config_entries.OptionsFlow):
    """Handle Zeversolar options."""

    def __init__(self, config_entry):
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_URL,
                        default=self.config_entry.data.get(CONF_URL, DEFAULT_URL),
                    ): str,
                }
            ),
        )
