#!/bin/sh
# Initialize Python environment
python -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Font configuration
ln -sf ${DEJAVU_FONT_DIR:-/nix/store/*-dejavu-fonts-*/share/fonts/truetype/dejavu} /usr/share/fonts/truetype/
fc-cache -f -v
