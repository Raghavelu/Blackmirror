with (import (fetchTarball "https://github.com/NixOS/nixpkgs/archive/23.11.tar.gz") {});
pkgs.mkShell {
    buildInputs = [
        pkgs.python311
        pkgs.python311Packages.pip
        pkgs.dejavu_fonts
        pkgs.fontconfig
        pkgs.gunicorn
    ];
}
