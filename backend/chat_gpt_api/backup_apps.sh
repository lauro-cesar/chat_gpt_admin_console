#!/bin/bash
source .venv/bin/activate
# shellcheck disable=SC2034
export app_list=$(cat backup_list.txt)

hora=$(date +%Y_%m_%d_%H)
# shellcheck disable=SC2043
for app in $app_list;
  do
    # shellcheck disable=SC2086
    mkdir -p bks/$app
    mkdir -p initial_data
    # shellcheck disable=SC2086
    python manage.py dumpdata --indent 4 $app > "bks/$app/$hora.json";
    SIZE=$(stat -c%s "bks/$app/$hora.json")
    if [ "$SIZE" -gt 4 ]; then
      rsync -azv  "bks/$app/$hora.json" "initial_data/$app.json"
    fi
  done