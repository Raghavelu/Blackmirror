with (import (fetchTarball "https://github.com/NixOS/nixpkgs/archive/23.11.tar.gz") {});
pkgs.mkShell {
    buildInputs = [
        pkgs.python311
        pkgs.python311Packages.pip
        pkgs.python311Packages.gunicorn
        pkgs.dejavu_fonts
        pkgs.fontconfig
        pkgs.zlib
        pkgs.stdenv.cc.cc.lib  # C compiler utilities
        pkgs.linuxPackages.nvidia_x11  # For numpy acceleration
    ];
}
