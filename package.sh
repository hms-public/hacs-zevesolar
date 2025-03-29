#!/bin/bash
# Package the Zeversolar integration for distribution

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Zeversolar Home Assistant Integration Packager${NC}"

# Create a temporary directory
TEMP_DIR=$(mktemp -d)
PACKAGE_DIR="$TEMP_DIR/zeversolar"
mkdir -p "$PACKAGE_DIR/custom_components/zeversolar/translations"

# Copy the necessary files
echo "Copying files..."
# Core integration files
cp custom_components/zeversolar/__init__.py "$PACKAGE_DIR/custom_components/zeversolar/"
cp custom_components/zeversolar/config_flow.py "$PACKAGE_DIR/custom_components/zeversolar/"
cp custom_components/zeversolar/const.py "$PACKAGE_DIR/custom_components/zeversolar/"
cp custom_components/zeversolar/manifest.json "$PACKAGE_DIR/custom_components/zeversolar/"
cp custom_components/zeversolar/sensor.py "$PACKAGE_DIR/custom_components/zeversolar/"
cp custom_components/zeversolar/translations/en.json "$PACKAGE_DIR/custom_components/zeversolar/translations/"

# Root level files
cp README.md "$PACKAGE_DIR/"
cp LICENSE "$PACKAGE_DIR/"
cp info.md "$PACKAGE_DIR/"
cp install.sh "$PACKAGE_DIR/"
cp hacs.json "$PACKAGE_DIR/"

# Create the zip file
echo "Creating zip file..."
CURRENT_DIR=$(pwd)
cd "$TEMP_DIR"
zip -r "$CURRENT_DIR/zeversolar_integration.zip" zeversolar
cd "$CURRENT_DIR"

# Clean up
rm -rf "$TEMP_DIR"

echo -e "${GREEN}Package created: zeversolar_integration.zip${NC}"
echo "You can distribute this zip file to users for installation."
echo "Users can extract the zip file and run the install.sh script to install the integration."
