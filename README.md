# Zeversolar Integration for Home Assistant

This custom component integrates Zeversolar inverters into Home Assistant, allowing you to monitor your solar power generation.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitLab](https://img.shields.io/badge/GitLab-Repository-orange.svg)](https://gitlab.com/hms-public/homeassistant/hacs/zeversolar)

## Features

- Displays current power output (in Watts)
- Shows energy generated today (in kWh)
- Provides inverter status and device information
- Configurable URL for connecting to your Zeversolar device
- Handles inverter offline periods (between dusk and sunrise) gracefully
- Dedicated inverter status sensor to monitor online/offline state

## Installation

### HACS (Home Assistant Community Store)

1. Ensure HACS is installed in your Home Assistant instance
2. Go to HACS > Integrations
3. Click the three dots in the top right corner and select "Custom repositories"
4. Add the URL of this repository and select "Integration" as the category
5. Click "Add"
6. Search for "Zeversolar" in the integrations tab
7. Click "Install"
8. Restart Home Assistant

### Manual Installation

1. Download the `custom_components/zeversolar` directory from this repository
2. Copy the directory to your Home Assistant's `custom_components` directory
3. Restart Home Assistant

## Configuration

1. Go to Configuration > Integrations
2. Click the "+ Add Integration" button
3. Search for "Zeversolar"
4. Enter the URL of your Zeversolar device (e.g., http://zeversolar.hms-srv.com)
5. Click "Submit"

## Sensors

This integration provides the following sensors:

- **Current Power**: The current power output of your solar inverter in Watts
- **Energy Today**: The total energy generated today in kilowatt-hours (kWh)
- **Inverter Status**: The current status of the inverter (Online, Offline, Error, etc.)

Each sensor includes additional attributes:
- Serial Number
- Registry Key
- Hardware Version
- Software Version
- Inverter Status

## Offline Handling

The integration is designed to handle periods when the inverter is offline (typically between dusk and sunrise):

- When the inverter is offline, the integration will continue to function
- The Current Power sensor will show 0 watts
- The Energy Today sensor will retain its last known value
- The Inverter Status sensor will show "Offline"
- All sensors remain available for automations and history tracking

This ensures that your Home Assistant dashboards and automations continue to work even when the inverter is not producing power.

## Troubleshooting

If you encounter issues with the integration:

1. Check that your Zeversolar device is online and accessible from your Home Assistant instance
2. Verify that the URL you provided is correct
3. Check the Home Assistant logs for any error messages related to the Zeversolar integration
4. If the inverter is offline (at night), this is normal behavior - the integration will show 0 watts and "Offline" status

## Support

If you need help or want to report a bug, please open an issue on the [GitLab repository](https://gitlab.com/hms-public/homeassistant/hacs/zeversolar/-/issues).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
