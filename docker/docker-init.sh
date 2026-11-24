#!/bin/bash
set -e

superset db upgrade

superset fab create-admin \
  --username "${SUPERSET_ADMIN_USERNAME:-admin}" \
  --firstname "${SUPERSET_ADMIN_FIRSTNAME:-Admin}" \
  --lastname "${SUPERSET_ADMIN_LASTNAME:-User}" \
  --email "${SUPERSET_ADMIN_EMAIL:-admin@local.test}" \
  --password "${SUPERSET_ADMIN_PASSWORD:-Rushi@22}" 2>/dev/null || true

superset init
