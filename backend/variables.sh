#!/bin/bash
set +x
for l in $(cat .env-project.yaml); do export "$l"; done
for l in $(cat .env-db.yaml); do export "$l"; done
for l in $(cat .env-api.yaml); do export "$l"; done
for l in $(cat .env-common.yaml); do export "$l"; done
for l in $(cat .env-redis-queue.yaml); do export "$l"; done
for l in $(cat .env-redis-cache.yaml); do export "$l"; done
for l in $(cat .env-redis-channels.yaml); do export "$l"; done
for l in $(cat .env-nginx.yaml); do export "$l"; done