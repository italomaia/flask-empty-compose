#!/bin/bash
set -e

# copies template and replaces variables
envsubst < traefik.toml > /etc/traefik/traefik.toml

exec "$@"