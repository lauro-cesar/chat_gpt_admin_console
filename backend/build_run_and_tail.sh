#!/bin/bash
set -x
source variables.sh

echo "Build Docker"

docker compose -p $DOCKER_NAME down -v
docker compose -p $DOCKER_NAME build
docker compose -p $DOCKER_NAME up