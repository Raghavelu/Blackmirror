with (import (fetchTarball "https://github.com/NixOS/nixpkgs/archive/23.11.tar.gz") {});

let
  pythonEnv = pkgs.python311.withPackages (ps: with ps; [
    flask
    openai
    fpdf2
    python-dotenv
    requests
    gunicorn
    python-dateutil
    gevent
    numpy
    chardet
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
    # Create startup script in standard location
    mkdir -p /usr/local/bin
    cat > /usr/local/bin/start-app <<EOF
    #!/bin/sh
    export PATH="${pythonEnv}/bin:\$PATH"
    export PYTHONPATH="${pythonEnv}/${pythonEnv.sitePackages}"
    export FONTCONFIG_FILE="${pkgs.fontconfig}/etc/fonts/fonts.conf"
    export FPDF_FONT_DIR="/app/fonts"
    
    # Verify critical paths
    echo "=== Startup Verification ==="
    which gunicorn
    ls -l /app/fonts/DejaVuSans.ttf
    echo "============================"
    
    exec gunicorn main:app --timeout 300 --bind 0.0.0.0:\$PORT
    EOF
    
    # Set permissions and verify
    chmod +x /usr/local/bin/start-app
    echo "Start script created at:"
    ls -l /usr/local/bin/start-app
  '';
}
