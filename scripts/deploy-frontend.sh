#!/usr/bin/env bash
set -euo pipefail

: "${FRONTEND_HOST:?Define FRONTEND_HOST, por ejemplo 192.168.131.37}"
: "${FRONTEND_USER:?Define FRONTEND_USER con el usuario SSH de la otra PC}"
: "${BACKEND_URL:?Define BACKEND_URL, por ejemplo http://192.168.131.192:5000}"
REMOTE_DIR="${REMOTE_DIR:-~/calculadora-frontend}"

ssh "${FRONTEND_USER}@${FRONTEND_HOST}" "mkdir -p ${REMOTE_DIR}/frontend"
scp docker-compose.frontend.yml "${FRONTEND_USER}@${FRONTEND_HOST}:${REMOTE_DIR}/"
scp frontend/Dockerfile frontend/index.html frontend/nginx.conf frontend/entrypoint.sh \
  "${FRONTEND_USER}@${FRONTEND_HOST}:${REMOTE_DIR}/frontend/"
ssh "${FRONTEND_USER}@${FRONTEND_HOST}" \
  "cd ${REMOTE_DIR} && BACKEND_URL=${BACKEND_URL} docker compose -f docker-compose.frontend.yml up -d --build"

echo "Frontend deployed on ${FRONTEND_HOST}:8080"