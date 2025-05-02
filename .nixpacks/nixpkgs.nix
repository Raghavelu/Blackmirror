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
    # Direct font path export
    export FPDF_FONT_DIR="${pkgs.dejavu_fonts}/share/fonts/truetype/dejavu"
    export FONTCONFIG_FILE="${pkgs.fontconfig}/etc/fonts/fonts.conf"
    
    # Verify font existence
    echo "Font verification:"
    ls -l ${pkgs.dejavu_fonts}/share/fonts/truetype/dejavu/DejaVuSans.ttf
    fc-list | grep DejaVu
  '';
}
