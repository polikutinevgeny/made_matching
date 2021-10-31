#!/usr/bin/env bash
set -e

docker-compose -f docker/prod/docker-compose.yml --project-directory . up --build -d
