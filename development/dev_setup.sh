#!/bin/bash
# Development setup script for Zeversolar Home Assistant integration

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Zeversolar Home Assistant Integration Development Setup${NC}"
echo "This script will set up a development environment for the Zeversolar integration."

# Check if python3 is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: python3 is not installed.${NC}"
    echo "Please install python3 and try again."
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo -e "${RED}Error: pip3 is not installed.${NC}"
    echo "Please install pip3 and try again."
    exit 1
fi

# Create a virtual environment
echo "Creating a virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip3 install requests voluptuous

# Run the test script
echo "Running the test script..."
python3 test_zeversolar.py

echo -e "${GREEN}Development setup complete!${NC}"
echo "You can now modify the code and test it using the test script."
echo "To activate the virtual environment in the future, run:"
echo "  source venv/bin/activate"
echo ""
echo "To test the integration, run:"
echo "  python3 test_zeversolar.py"
