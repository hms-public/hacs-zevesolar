#!/bin/bash
# Installation script for Zeversolar Home Assistant integration

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Zeversolar Home Assistant Integration Installer${NC}"
echo "This script will install the Zeversolar integration to your Home Assistant instance."

# Check if HASS_CONFIG_DIR is set, otherwise use default
if [ -z "$HASS_CONFIG_DIR" ]; then
    echo -e "${YELLOW}HASS_CONFIG_DIR environment variable not set.${NC}"
    echo "Please enter the path to your Home Assistant configuration directory:"
    echo "For example: /config or ~/.homeassistant"
    read -p "> " HASS_CONFIG_DIR
fi

# Validate the directory exists
if [ ! -d "$HASS_CONFIG_DIR" ]; then
    echo -e "${RED}Error: Directory $HASS_CONFIG_DIR does not exist.${NC}"
    echo "Please check the path and try again."
    exit 1
fi

# Check if custom_components directory exists, create if not
CUSTOM_COMPONENTS_DIR="$HASS_CONFIG_DIR/custom_components"
if [ ! -d "$CUSTOM_COMPONENTS_DIR" ]; then
    echo "Creating custom_components directory..."
    mkdir -p "$CUSTOM_COMPONENTS_DIR"
fi

# Create zeversolar directory
ZEVERSOLAR_DIR="$CUSTOM_COMPONENTS_DIR/zeversolar"
if [ -d "$ZEVERSOLAR_DIR" ]; then
    echo -e "${YELLOW}Warning: Zeversolar directory already exists. Overwriting...${NC}"
    rm -rf "$ZEVERSOLAR_DIR"
fi

echo "Installing Zeversolar integration..."
mkdir -p "$ZEVERSOLAR_DIR/translations"

# Copy files from the custom_components directory
cp -r custom_components/zeversolar/* "$ZEVERSOLAR_DIR/"

# Make sure LICENSE file is included
if [ ! -f "$ZEVERSOLAR_DIR/LICENSE" ] && [ -f "LICENSE" ]; then
    echo "Copying LICENSE file..."
    cp LICENSE "$ZEVERSOLAR_DIR/"
fi

echo -e "${GREEN}Installation complete!${NC}"
echo "To use the integration:"
echo "1. Restart Home Assistant"
echo "2. Go to Configuration > Integrations"
echo "3. Click the '+ Add Integration' button"
echo "4. Search for 'Zeversolar'"
echo "5. Enter the URL of your Zeversolar device"
echo ""
echo -e "${YELLOW}Note:${NC} If you don't see the integration in the list, clear your browser cache and try again."
