#!/bin/sh
set -e

# copies template and replaces variables
envsubst < /etc/nginx/conf.d/default.template > /etc/nginx/conf.d/default.conf

exec "$@"