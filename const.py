"""Constants for the Zeversolar integration."""

DOMAIN = "zeversolar"

# Configuration
CONF_URL = "url"
DEFAULT_URL = "http://zeversolar.hms-srv.com"
DEFAULT_NAME = "Zeversolar"
DEFAULT_SCAN_INTERVAL = 60  # seconds

# Attributes
ATTR_SERIAL_NUMBER = "serial_number"
ATTR_REGISTRY_ID = "registry_id"
ATTR_REGISTRY_KEY = "registry_key"
ATTR_HARDWARE_VERSION = "hardware_version"
ATTR_SOFTWARE_VERSION = "software_version"
ATTR_INVERTER_STATUS = "inverter_status"
ATTR_LAST_UPDATED = "last_updated"

# Sensor types
SENSOR_TYPES = {
    "current_power": {
        "name": "Current Power",
        "unit": "W",
        "icon": "mdi:solar-power",
        "device_class": "power",
        "state_class": "measurement",
    },
    "energy_today": {
        "name": "Energy Today",
        "unit": "kWh",
        "icon": "mdi:solar-power",
        "device_class": "energy",
        "state_class": "total_increasing",
    },
}
