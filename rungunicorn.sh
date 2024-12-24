#!/usr/bin/env bash
set -ex -o pipefail
gunicorn -c ${APP_ROOT}/gunicorn_config.py --access-logfile - --error-logfile - whatsapp_integration.wsgi:application