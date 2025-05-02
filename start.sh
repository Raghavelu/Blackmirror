#!/bin/sh
export PYTHONPATH=$PYTHONPATH:${pythonEnv}/${pythonEnv.sitePackages}
exec gunicorn main:app --timeout 300 --bind 0.0.0.0:$PORT
