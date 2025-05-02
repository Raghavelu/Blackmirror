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
    # Set critical environment variables
    export PATH="${pythonEnv}/bin:$PATH"
    export PYTHONPATH="${pythonEnv}/${pythonEnv.sitePackages}"
    export FONTCONFIG_FILE="${pkgs.fontconfig.out}/etc/fonts/fonts.conf"
  '';
}
