[phases.setup]
nixPkgs = [
    "python311",
    "python311Packages.pip",
    "python311Packages.gunicorn",
    "dejavu_fonts",
    "fontconfig",
    "zlib",
    "stdenv.cc.cc.lib",
    "linuxPackages.nvidia_x11"
]

[phases.install]
commands = [
    "python -m pip install --upgrade pip setuptools wheel",
    "pip install --no-cache-dir -r requirements.txt",
    "fc-cache -f -v"
]

[phases.start]
cmd = "gunicorn main:app --timeout 300 --bind 0.0.0.0:$PORT"
