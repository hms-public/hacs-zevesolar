# Changelog

## 0.1.2 (2025-04-02)

### Fixed
- Fixed issue with negative energy values appearing in the morning. The integration now properly handles the daily reset of the inverter's energy counter, preventing negative spikes in the energy dashboard.

## 0.1.1 (2025-03-31)

### Fixed
- Fixed energy reporting in Home Assistant energy dashboard by changing the state_class of energy_today sensor from "total_increasing" to "total". This prevents Home Assistant from incorrectly accumulating daily energy values and displaying exaggerated generation amounts.

## 0.1.0 (Initial Release)

### Added
- Initial release of the Zeversolar integration for Home Assistant
- Support for monitoring current power output and energy generated today
- Dedicated inverter status sensor
- Graceful handling of inverter offline periods
