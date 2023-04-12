#!/bin/bash

rsync -azv  --exclude=".python3/*" --exclude="bks/*" --exclude=".git/" --exclude=".venv/*" --exclude=".env/*"  --exclude=".cache/*"  --exclude="migrations/"  backend/ -e 'ssh' app@143.42.129.28:/home/app/console/