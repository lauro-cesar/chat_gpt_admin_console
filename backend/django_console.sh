#!/bin/bash
set -x

source variables.sh

echo "Run Docker Django bash"

docker compose -p $DOCKER_NAME exec $DJANGO_SERVICE_NAME bash
