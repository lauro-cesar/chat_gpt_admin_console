#!/bin/bash
set -x
source variables.sh
echo "Run Docker"
docker compose -p $DOCKER_NAME up
