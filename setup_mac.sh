#!/bin/bash
echo "Setting up JarviSonix Music App on macOS..."

# Create virtual environments
echo "Creating Python 3.11 environment for basic-pitch..."
python3.11 -m venv venv_basic_pitch
source venv_basic_pitch/bin/activate
pip install --upgrade pip
pip install -r requirements_basic_pitch.txt

echo "Creating Python 3.13 environment for CUA..."
python3.13 -m venv venv_cua
source venv_cua/bin/activate
pip install --upgrade pip
pip install -r requirements_cua.txt

# Install main requirements in current environment
echo "Installing main requirements..."
pip install -r requirements.txt

echo "Setup complete!"
echo ""
echo "To run the app:"
echo "1. Start the GUI: python front-end/app.py"
echo "2. Or run directly: python listen.py"
echo ""
