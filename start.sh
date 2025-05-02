#!/bin/bash
set -e

echo "[ENTRYPOINT] Setting up Python environment..."

# Make sure fonts are available
fc-cache -f -v
ln -sf /nix/store/*-dejavu-fonts-*/share/fonts/truetype/dejavu /app/fonts

# Force export pythonEnv bin into PATH
export PATH=$(find /nix/store -type d -name "bin" | grep python3 | head -n 1):$PATH

echo "[ENTRYPOINT] PATH is $PATH"
which gunicorn
gunicorn main:app --timeout 300 --bind 0.0.0.0:$PORT
