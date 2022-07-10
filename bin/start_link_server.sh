#!/bin/bash
set -x

export FLASK_APP=link_server
export FLASK_RUN_PORT=3000

flask run
