with (import (fetchTarball "https://github.com/NixOS/nixpkgs/archive/23.11.tar.gz") {});
pkgs.mkShell {
    buildInputs = [
        dejavu_fonts
        fontconfig
    ];
}
