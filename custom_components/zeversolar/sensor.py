"""Support for Zeversolar sensors."""
import logging
from datetime import datetime, date

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    DOMAIN,
    SENSOR_TYPES,
    ATTR_SERIAL_NUMBER,
    ATTR_REGISTRY_KEY,
    ATTR_HARDWARE_VERSION,
    ATTR_SOFTWARE_VERSION,
    ATTR_INVERTER_STATUS,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
):
    """Set up Zeversolar sensor based on a config entry."""
    coordinator = hass.data[DOMAIN][entry.entry_id]

    # Wait for coordinator to get data
    await coordinator.async_config_entry_first_refresh()

    entities = []
    for sensor_type in SENSOR_TYPES:
        entities.append(ZeversolarSensor(coordinator, sensor_type, entry))

    # Add an additional sensor for inverter status
    entities.append(ZeversolarStatusSensor(coordinator, entry))

    async_add_entities(entities)


class ZeversolarSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Zeversolar sensor."""

    def __init__(self, coordinator, sensor_type, entry):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._sensor_type = sensor_type
        self._config_entry = entry
        self._attr_name = f"{SENSOR_TYPES[sensor_type]['name']}"
        self._attr_unique_id = f"{entry.entry_id}_{sensor_type}"
        self._attr_native_unit_of_measurement = SENSOR_TYPES[sensor_type]["unit"]
        self._attr_icon = SENSOR_TYPES[sensor_type]["icon"]
        self._attr_device_class = SENSOR_TYPES[sensor_type]["device_class"]
        self._attr_state_class = SENSOR_TYPES[sensor_type]["state_class"]
        
        # For tracking energy values and daily accumulators
        self._previous_energy_today = None
        self._today_accumulated_energy = 0
        self._last_reset_date = None

    @property
    def device_info(self):
        """Return device information about this Zeversolar device."""
        if not self.coordinator.data:
            return None

        return DeviceInfo(
            identifiers={(DOMAIN, self.coordinator.data.get("serial_number", "unknown"))},
            name="Zeversolar Inverter",
            manufacturer="Zeversolar",
            model=self.coordinator.data.get("hardware_version", "unknown"),
            sw_version=self.coordinator.data.get("software_version", "unknown"),
        )

    @property
    def native_value(self):
        """Return the state of the sensor."""
        if not self.coordinator.data:
            return None

        current_datetime = datetime.now()
        current_date = current_datetime.date()
        
        if self._sensor_type == "current_power":
            # Just return the current power value directly
            return self.coordinator.data.get("current_power", 0)
            
        elif self._sensor_type == "energy_today":
            # Just return the raw energy value from the inverter
            return self.coordinator.data.get("energy_today", 0)
            
        elif self._sensor_type == "energy_today_total":
            # Get the current energy value
            current_value = self.coordinator.data.get("energy_today", 0)
            inverter_status = self.coordinator.data.get("inverter_status", "Unknown")
            
            # First reading ever
            if self._previous_energy_today is None:
                self._previous_energy_today = current_value
                self._last_reset_date = current_date
                self._today_accumulated_energy = current_value
                return current_value
                
            # Check for date change (midnight reset)
            if self._last_reset_date != current_date:
                _LOGGER.info(
                    "Daily date change detected: previous_date=%s, current_date=%s", 
                    self._last_reset_date, 
                    current_date
                )
                # It's a new day, reset accumulators
                self._last_reset_date = current_date
                # Start counting from the current value on the new day
                self._today_accumulated_energy = current_value
                self._previous_energy_today = current_value
                return current_value
                
            # Check for inverter reset
            # This happens when the current value is much lower than the previous value
            # and the inverter just came back online after being offline or reset at midnight
            if current_value < self._previous_energy_today and (self._previous_energy_today - current_value) > 0.5:
                _LOGGER.info(
                    "Inverter reset detected: previous=%s, current=%s, status=%s", 
                    self._previous_energy_today, 
                    current_value, 
                    inverter_status
                )
                
                # If it's a reset, we just start accumulating from the current value
                # without adding the negative delta to our accumulator
                self._today_accumulated_energy = current_value
            else:
                # Normal operation - accumulate any positive delta
                if current_value > self._previous_energy_today:
                    # Only add positive changes to the accumulator
                    delta = current_value - self._previous_energy_today
                    self._today_accumulated_energy += delta
            
            # Update previous value for next time
            self._previous_energy_today = current_value
            
            # Return the accumulated value
            return self._today_accumulated_energy
            
        return None

    @property
    def available(self):
        """Return True if entity is available."""
        # The sensor is always available, even when the inverter is offline
        return self.coordinator.last_successful_data is not None or self.coordinator.data is not None

    @property
    def extra_state_attributes(self):
        """Return the state attributes of the device."""
        if not self.coordinator.data:
            return None

        return {
            ATTR_SERIAL_NUMBER: self.coordinator.data.get("inverter_serial", "unknown"),
            ATTR_REGISTRY_KEY: self.coordinator.data.get("registry_key", "unknown"),
            ATTR_HARDWARE_VERSION: self.coordinator.data.get("hardware_version", "unknown"),
            ATTR_SOFTWARE_VERSION: self.coordinator.data.get("software_version", "unknown"),
            ATTR_INVERTER_STATUS: self.coordinator.data.get("inverter_status", "unknown"),
        }


class ZeversolarStatusSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Zeversolar status sensor."""

    def __init__(self, coordinator, entry):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._config_entry = entry
        self._attr_name = "Inverter Status"
        self._attr_unique_id = f"{entry.entry_id}_inverter_status"
        self._attr_icon = "mdi:solar-power"

    @property
    def device_info(self):
        """Return device information about this Zeversolar device."""
        if not self.coordinator.data:
            return None

        return DeviceInfo(
            identifiers={(DOMAIN, self.coordinator.data.get("serial_number", "unknown"))},
            name="Zeversolar Inverter",
            manufacturer="Zeversolar",
            model=self.coordinator.data.get("hardware_version", "unknown"),
            sw_version=self.coordinator.data.get("software_version", "unknown"),
        )

    @property
    def native_value(self):
        """Return the state of the sensor."""
        if not self.coordinator.data:
            return "Unknown"

        return self.coordinator.data.get("inverter_status", "Unknown")

    @property
    def available(self):
        """Return True if entity is available."""
        # The status sensor is always available
        return True

    @property
    def extra_state_attributes(self):
        """Return the state attributes of the device."""
        if not self.coordinator.data:
            return None

        return {
            ATTR_SERIAL_NUMBER: self.coordinator.data.get("inverter_serial", "unknown"),
            ATTR_REGISTRY_KEY: self.coordinator.data.get("registry_key", "unknown"),
            ATTR_HARDWARE_VERSION: self.coordinator.data.get("hardware_version", "unknown"),
            ATTR_SOFTWARE_VERSION: self.coordinator.data.get("software_version", "unknown"),
        }
