#!/usr/bin/env python3
"""
Test script for the Zeversolar integration.
This script fetches data from a Zeversolar device and prints it to the console.
"""
import argparse
import requests
import sys


def fetch_zeversolar_data(url):
    """Fetch data from a Zeversolar device."""
    try:
        response = requests.get(f"{url}/home.cgi", timeout=10)
        response.raise_for_status()
        
        data = response.text.strip().split("\n")
        
        if len(data) < 9:
            print("Error: Invalid data received from Zeversolar device")
            return None
            
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
        }
        
        # Parse inverter data if available
        if int(data[8]) > 0:
            inverter_index = 9
            result["inverter_serial"] = data[inverter_index]
            result["current_power"] = int(data[inverter_index + 1])
            result["energy_today"] = float(data[inverter_index + 2])
            result["inverter_status"] = data[inverter_index + 3]
        
        return result
    except requests.RequestException as error:
        print(f"Error fetching data from Zeversolar: {error}")
        return None


def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Test Zeversolar integration")
    parser.add_argument("--url", default="http://zeversolar.hms-srv.com",
                        help="URL of the Zeversolar device")
    args = parser.parse_args()
    
    print(f"Fetching data from {args.url}...")
    data = fetch_zeversolar_data(args.url)
    
    if data:
        print("\nZeversolar Device Information:")
        print(f"Serial Number: {data.get('serial_number')}")
        print(f"Registry Key: {data.get('registry_key')}")
        print(f"Hardware Version: {data.get('hardware_version')}")
        print(f"Software Version: {data.get('software_version')}")
        print(f"Time: {data.get('time')}")
        print(f"Cloud Status: {'OK' if data.get('cloud_status') == '0' else 'Error'}")
        
        if "inverter_serial" in data:
            print("\nInverter Information:")
            print(f"Inverter Serial: {data.get('inverter_serial')}")
            print(f"Current Power: {data.get('current_power')} W")
            print(f"Energy Today: {data.get('energy_today')} kWh")
            print(f"Inverter Status: {data.get('inverter_status')}")
        
        return 0
    else:
        return 1


if __name__ == "__main__":
    sys.exit(main())
