# Zeversolar Integration for Home Assistant

This custom component integrates Zeversolar inverters into Home Assistant, allowing you to monitor your solar power generation.

## Features

- Displays current power output (in Watts)
- Shows energy generated today (in kWh)
- Provides inverter status and device information
- Configurable URL for connecting to your Zeversolar device
- Handles inverter offline periods (between dusk and sunrise) gracefully
- Dedicated inverter status sensor to monitor online/offline state
- Allows configuration even when the inverter is offline
- Correctly reports daily energy values in Home Assistant energy dashboard

## Latest Update (v0.1.2)

- Fixed issue with negative energy values appearing in the morning
- Fixed energy reporting in Home Assistant energy dashboard
- See [CHANGELOG](CHANGELOG.md) for full details

## Configuration

1. Go to Configuration > Integrations
2. Click the "+ Add Integration" button
3. Search for "Zeversolar"
4. Enter the URL of your Zeversolar device (e.g., http://zeverinverter.example.com or local IP address)
5. Click "Submit"

**Note:** The integration can be configured even when the inverter is offline. You'll see a warning message, but the integration will be added and will start working once the inverter comes online.

## Offline Handling

The integration is designed to handle periods when the inverter is offline (typically between dusk and sunrise). When the inverter is offline, the integration will continue to function with the Current Power sensor showing 0 watts and the Inverter Status sensor showing "Offline".
