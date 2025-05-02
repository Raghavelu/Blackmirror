with (import (fetchTarball "https://github.com/NixOS/nixpkgs/archive/23.11.tar.gz") {});
pkgs.mkShell {
    buildInputs = [
        pkgs.python311
        # Python packages
        pkgs.python311Packages.flask
        pkgs.python311Packages.openai
        pkgs.python311Packages.fpdf2
        pkgs.python311Packages.python-dotenv
        pkgs.python311Packages.requests
        pkgs.python311Packages.gunicorn
        pkgs.python311Packages.python-dateutil
        pkgs.python311Packages.gevent
        pkgs.python311Packages.numpy
        pkgs.python311Packages.chardet
        
        # System dependencies
        pkgs.dejavu_fonts
        pkgs.fontconfig
        pkgs.zlib
        pkgs.stdenv.cc.cc.lib
    ];
}
