#!/bin/bash
set -x
source variables.sh
export DEBUG=1

source .venv/bin/activate && cd $PROJECT_DIR && python3 manage.py runserver

