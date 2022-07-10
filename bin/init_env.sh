#!/bin/bash
set -x

deactivate 2>/dev/null  # silently fail when no venv active
rm -rf env
python3 -m venv env
source env/bin/activate
pip3 install -r requirements.txt
