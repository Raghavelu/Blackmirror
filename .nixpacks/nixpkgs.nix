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
    export PATH="${pythonEnv}/bin:$PATH"
    export PYTHONPATH="${pythonEnv}/${pythonEnv.sitePackages}"
    export FONTCONFIG_FILE="${pkgs.fontconfig}/etc/fonts/fonts.conf"

    echo "=== Installed Python Packages ==="
    pip list
    echo "================================="
    which gunicorn || echo "Gunicorn not found in PATH"
  '';
}
