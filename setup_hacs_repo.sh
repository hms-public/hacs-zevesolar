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

# Create a temporary directory if needed
if [ "$1" != "--local" ]; then
    TEMP_DIR=$(mktemp -d)
    REPO_DIR="$TEMP_DIR/zeversolar"
    mkdir -p "$REPO_DIR/custom_components/zeversolar/translations"
    COPY_CMD="cp"
else
    REPO_DIR="."
    COPY_CMD="echo 'Using local directory, no need to copy files.'"
fi

# Copy or use the necessary files
echo "Preparing files..."

if [ "$1" != "--local" ]; then
    # Copy core files to the custom_components directory
    cp custom_components/zeversolar/__init__.py "$REPO_DIR/custom_components/zeversolar/"
    cp custom_components/zeversolar/config_flow.py "$REPO_DIR/custom_components/zeversolar/"
    cp custom_components/zeversolar/const.py "$REPO_DIR/custom_components/zeversolar/"
    cp custom_components/zeversolar/manifest.json "$REPO_DIR/custom_components/zeversolar/"
    cp custom_components/zeversolar/sensor.py "$REPO_DIR/custom_components/zeversolar/"
    
    # Copy translations
    cp custom_components/zeversolar/translations/en.json "$REPO_DIR/custom_components/zeversolar/translations/"
    
    # Copy the documentation files to the root
    cp README.md "$REPO_DIR/"
    cp LICENSE "$REPO_DIR/"
    cp info.md "$REPO_DIR/"
fi

# Create or update hacs.json
cat > "$REPO_DIR/hacs.json" << EOF
{
  "name": "Zeversolar",
  "content_in_root": false,
  "render_readme": true,
  "domains": ["sensor"],
  "homeassistant": "2023.1.0"
}
EOF

# If using a temporary directory, initialize git repository
if [ "$1" != "--local" ]; then
    # Initialize git repository
    echo "Initializing git repository..."
    cd "$REPO_DIR"
    git init
    git add .
    git commit -m "Initial HACS repository setup for Zeversolar integration"
    
    echo -e "${GREEN}HACS repository setup complete!${NC}"
    echo "The repository has been created at: $REPO_DIR"
    echo ""
    echo "To publish the repository to GitLab:"
    echo "1. The repository is already set up at: https://gitlab.com/hms-public/homeassistant/hacs/zeversolar"
    echo "2. Run the following commands:"
    echo "   cd $REPO_DIR"
    echo "   git remote add origin https://gitlab.com/hms-public/homeassistant/hacs/zeversolar.git"
    echo "   git push -u origin master"
else
    echo -e "${GREEN}HACS repository files updated in current directory.${NC}"
    echo "You can now commit these changes to your git repository."
fi

echo ""
echo "Once published, users can add it to HACS as a custom repository:"
echo "https://gitlab.com/hms-public/homeassistant/hacs/zeversolar"
