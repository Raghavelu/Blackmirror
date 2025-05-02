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
    # Create font symlinks using wildcard path
    mkdir -p /app/fonts
    ln -sf /nix/store/*-dejavu-fonts-*/share/fonts/truetype/dejavu/* /app/fonts/
    
    # Verify font installation
    echo "Font files in /app/fonts:"
    ls -l /app/fonts/DejaVuSans.ttf
  '';
}
