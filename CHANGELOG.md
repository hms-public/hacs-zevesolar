# Changelog

## 0.1.3 (2025-04-07)

### Changed
- Complete redesign of energy reporting system to eliminate negative values:
  - Added a new "Energy Today Total" sensor with state_class "total_increasing" for proper energy dashboard integration
  - Changed the original "Energy Today" sensor to use state_class "measurement" to prevent Home Assistant from trying to integrate it
  - Implemented date-based daily reset detection to properly handle the transition between days
  - Added sophisticated detection of inverter resets to prevent negative energy reporting
  - Implemented energy accumulation logic to ensure accurate daily production totals

## 0.1.2 (2025-04-02)

### Fixed
- Attempted fix for issue with negative energy values appearing in the morning (only partially successful).

## 0.1.1 (2025-03-31)

### Fixed
- Fixed energy reporting in Home Assistant energy dashboard by changing the state_class of energy_today sensor from "total_increasing" to "total". This prevents Home Assistant from incorrectly accumulating daily energy values and displaying exaggerated generation amounts.

## 0.1.0 (Initial Release)

### Added
- Initial release of the Zeversolar integration for Home Assistant
- Support for monitoring current power output and energy generated today
- Dedicated inverter status sensor
- Graceful handling of inverter offline periods
