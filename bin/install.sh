#!/bin/bash

# to be run in the same directory as "setup.py"

# Must use this unless there is an official release
development_build()
{
  python3 -m venv env
  source env/bin/activate
  pip install --upgrade pip
  pip install -e .
  chmod +x bin/*.sh
}

development_build_uninstall()
{
  rm -rf env/ subtitle-downloader.egg-info/
  pip uninstall .
}

# Version to use if offical release ever happens
production_build()
{
  pip install subtitle-downloader
}

if [ $1 = "uninstall" ]; then
  development_build_uninstall
  exit 0
fi

if [ $1 = "reinstall" ]; then
  development_build_uninstall
fi

development_build
