#!/bin/bash
set -e

# copies template and replaces variables
envsubst < nginx.conf > /etc/nginx/conf.d/default.conf

exec "$@"