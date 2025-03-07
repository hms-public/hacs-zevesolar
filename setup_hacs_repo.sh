#!/bin/bash
# Setup a HACS-compatible repository for the Zeversolar integration

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Zeversolar Home Assistant Integration HACS Repository Setup${NC}"
echo "This script will set up a HACS-compatible repository for the Zeversolar integration."

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo -e "${RED}Error: git is not installed.${NC}"
    echo "Please install git and try again."
    exit 1
fi

# Create a temporary directory
TEMP_DIR=$(mktemp -d)
REPO_DIR="$TEMP_DIR/zeversolar"
mkdir -p "$REPO_DIR/custom_components/zeversolar/translations"

# Copy the necessary files
echo "Copying files..."
cp __init__.py "$REPO_DIR/custom_components/zeversolar/"
cp config_flow.py "$REPO_DIR/custom_components/zeversolar/"
cp const.py "$REPO_DIR/custom_components/zeversolar/"
cp manifest.json "$REPO_DIR/custom_components/zeversolar/"
cp sensor.py "$REPO_DIR/custom_components/zeversolar/"
cp README.md "$REPO_DIR/"
cp LICENSE "$REPO_DIR/"
cp translations/en.json "$REPO_DIR/custom_components/zeversolar/translations/"

# Create hacs.json
cat > "$REPO_DIR/hacs.json" << EOF
{
  "name": "Zeversolar",
  "content_in_root": false,
  "render_readme": true,
  "domains": ["sensor"],
  "homeassistant": "2023.1.0"
}
EOF

# Create info.md
cat > "$REPO_DIR/info.md" << EOF
# Zeversolar Integration for Home Assistant

This custom component integrates Zeversolar inverters into Home Assistant, allowing you to monitor your solar power generation.

## Features

- Displays current power output (in Watts)
- Shows energy generated today (in kWh)
- Provides inverter status and device information
- Configurable URL for connecting to your Zeversolar device

## Configuration

1. Go to Configuration > Integrations
2. Click the "+ Add Integration" button
3. Search for "Zeversolar"
4. Enter the URL of your Zeversolar device (e.g., http://zeversolar.hms-srv.com)
5. Click "Submit"
EOF

# Initialize git repository
echo "Initializing git repository..."
cd "$REPO_DIR"
git init
git add .
git commit -m "Initial commit"

echo -e "${GREEN}HACS repository setup complete!${NC}"
echo "The repository has been created at: $REPO_DIR"
echo ""
echo "To publish the repository to GitLab:"
echo "1. The repository is already set up at: https://gitlab.com/hms-public/homeassistant/custom_components/zeversolar"
echo "2. Run the following commands:"
echo "   cd $REPO_DIR"
echo "   git remote add origin https://gitlab.com/hms-public/homeassistant/custom_components/zeversolar.git"
echo "   git push -u origin master"
echo ""
echo "Once published, users can add it to HACS as a custom repository:"
echo "https://gitlab.com/hms-public/homeassistant/custom_components/zeversolar"
