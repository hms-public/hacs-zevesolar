"""The Zeversolar integration."""
import asyncio
import logging
from datetime import timedelta, datetime

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
import homeassistant.helpers.config_validation as cv
import voluptuous as vol
import requests

from .const import (
    DOMAIN,
    DEFAULT_SCAN_INTERVAL,
    CONF_URL,
    ATTR_INVERTER_STATUS,
)

_LOGGER = logging.getLogger(__name__)

PLATFORMS = ["sensor"]


async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the Zeversolar component."""
    hass.data.setdefault(DOMAIN, {})
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up Zeversolar from a config entry."""
    url = entry.data[CONF_URL]

    coordinator = ZeversolarDataUpdateCoordinator(hass, url)
    await coordinator.async_config_entry_first_refresh()

    hass.data[DOMAIN][entry.entry_id] = coordinator

    for platform in PLATFORMS:
        hass.async_create_task(
            hass.config_entries.async_forward_entry_setup(entry, platform)
        )

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a config entry."""
    unload_ok = all(
        await asyncio.gather(
            *[
                hass.config_entries.async_forward_entry_unload(entry, platform)
                for platform in PLATFORMS
            ]
        )
    )
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok


class ZeversolarDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching Zeversolar data."""

    def __init__(self, hass, url):
        """Initialize."""
        self.url = url
        self.data = {}
        self.last_successful_data = {}

        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=DEFAULT_SCAN_INTERVAL),
        )

    async def _async_update_data(self):
        """Update data via library."""
        try:
            return await self.hass.async_add_executor_job(self.fetch_data)
        except Exception as error:
            _LOGGER.error("Error communicating with Zeversolar: %s", error)
            # Return last successful data if available, otherwise return offline status
            if self.last_successful_data:
                offline_data = self.last_successful_data.copy()
                offline_data["inverter_status"] = "Offline"
                offline_data["current_power"] = 0
                return offline_data
            else:
                # Return minimal data structure with offline status
                return {
                    "serial_number": "unknown",
                    "registry_key": "unknown",
                    "hardware_version": "unknown",
                    "software_version": "unknown",
                    "time": datetime.now().strftime("%H:%M %d/%m/%Y"),
                    "inverter_status": "Offline",
                    "current_power": 0,
                    "energy_today": 0,
                    "inverter_serial": "unknown",
                }

    def fetch_data(self):
        """Fetch data from Zeversolar."""
        try:
            response = requests.get(f"{self.url}/home.cgi", timeout=10)
            response.raise_for_status()
            
            data = response.text.strip().split("\n")
            
            # Parse the data based on the format we observed
            result = {
                "wifi_enabled": data[0],
                "display_mode": data[1],
                "serial_number": data[2],
                "registry_key": data[3],
                "hardware_version": data[4],
                "software_version": data[5],
                "time": data[6],
                "cloud_status": data[7],
                "inverter_count": data[8],
                "inverter_status": "Online",
            }
            
            # Parse inverter data if available
            if int(data[8]) > 0:
                inverter_index = 9
                result["inverter_serial"] = data[inverter_index]
                result["current_power"] = int(data[inverter_index + 1])
                result["energy_today"] = float(data[inverter_index + 2])
                if data[inverter_index + 3] == "OK":
                    result["inverter_status"] = "Online"
                else:
                    result["inverter_status"] = data[inverter_index + 3]
            else:
                # No inverter data available
                result["inverter_serial"] = "unknown"
                result["current_power"] = 0
                result["energy_today"] = 0
                result["inverter_status"] = "No Data"
            
            # Store successful data for future use if connection fails
            self.last_successful_data = result.copy()
            
            return result
        except requests.RequestException as error:
            _LOGGER.error("Error fetching data from Zeversolar: %s", error)
            # Re-raise the exception to be handled by _async_update_data
            raise
