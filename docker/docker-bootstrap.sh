#!/bin/bash
set -e

if [ "$1" = "app-gunicorn" ]; then
  exec gunicorn \
    --bind "0.0.0.0:${SUPERSET_PORT:-8090}" \
    --workers "${GUNICORN_WORKERS:-2}" \
    --worker-class gthread \
    --threads "${GUNICORN_THREADS:-20}" \
    --timeout 60 \
    --limit-request-line 0 \
    --limit-request-field_size 0 \
    "superset.app:create_app()"
fi

if [ "$1" = "worker" ]; then
  exec celery --app=superset.tasks.celery_app:app worker --pool=prefork -O fair -c "${CELERYD_CONCURRENCY:-2}"
fi

if [ "$1" = "beat" ]; then
  exec celery --app=superset.tasks.celery_app:app beat --loglevel=INFO
fi

echo "Unknown service mode: $1" >&2
exit 1
