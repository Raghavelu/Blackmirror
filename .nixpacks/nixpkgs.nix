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
  
  fontConf = pkgs.writeText "fonts.conf" ''
    <?xml version="1.0"?>
    <!DOCTYPE fontconfig SYSTEM "fonts.dtd">
    <fontconfig>
      <dir>${pkgs.dejavu_fonts}/share/fonts/truetype</dir>
      <dir>/run/current-system/sw/share/X11/fonts</dir>
      <cachedir>/tmp/fontconfig/cache</cachedir>
    </fontconfig>
  '';
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
    # Font configuration
    export FONTCONFIG_FILE="${fontConf}"
    export FONTCONFIG_PATH="${pkgs.fontconfig.out}/etc/fonts/"
    
    # Link fonts to predictable path
    mkdir -p /app/fonts
    ln -sf ${pkgs.dejavu_fonts}/share/fonts/truetype/dejavu /app/fonts/
    
    # Rebuild font cache
    fc-cache -f -v
  '';
}
