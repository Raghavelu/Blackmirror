with (import (fetchTarball "https://github.com/NixOS/nixpkgs/archive/23.11.tar.gz") {});

let
  pythonEnv = pkgs.python311.withPackages (ps: [
    ps.flask
    ps.openai
    ps.fpdf2
    ps.python-dotenv
    ps.requests
    ps.gunicorn
    ps.python-dateutil
    ps.gevent
    ps.numpy
    ps.chardet
  ]);
in
pkgs.mkShell {
  buildInputs = [
    pythonEnv
    pkgs.dejavu_fonts
    pkgs.fontconfig
    pkgs.zlib
    pkgs.stdenv.cc.cc.lib
  ];

  shellHook = ''
    # Create start script directly in app directory
    mkdir -p /app
    cat > /app/start.sh <<EOF
    #!/bin/sh
    export FONTCONFIG_FILE=${pkgs.fontconfig.out}/etc/fonts/fonts.conf
    export FONTCONFIG_PATH=${pkgs.fontconfig.out}/etc/fonts/
    export PYTHONPATH="${pythonEnv}/${pythonEnv.sitePackages}"
    exec "${pythonEnv}/bin/gunicorn" main:app --timeout 300 --bind 0.0.0.0:\$PORT
    EOF
    chmod +x /app/start.sh
  '';
}
