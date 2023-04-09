#!/bin/bash
set -x
logger "Starting hourly backup"

cd "/home/django_project/" || exit

./backup_apps.sh

exit 0