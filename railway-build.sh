#!/bin/sh
# Initialize Nix environment
nix-channel --add https://nixos.org/channels/nixpkgs-23.11 nixpkgs
nix-channel --update

# Build using Nix dependencies
nix-build .nixpacks/nixpkgs.nix -o deps

# Link fonts
ln -sf deps/share/fonts/truetype/dejavu /usr/share/fonts/truetype/
fc-cache -f -v
