#!/bin/bash
python3 -m venv "lin_venv"
source "lin_venv/bin/activate"
./lin_venv/bin/pip install -r "requirements.txt"
apt-get install python3-tk
./lin_venv/bin/python "main.py"
