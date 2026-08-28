#!/usr/bin/env bash
set -euo pipefail

: "${DEPLOY_HOST:?Define DEPLOY_HOST con la IP o nombre del equipo destino}"
: "${DEPLOY_USER:?Define DEPLOY_USER con el usuario SSH destino}"
REMOTE_DIR="${REMOTE_DIR:-~/calculadora-confusa}"

ssh "${DEPLOY_USER}@${DEPLOY_HOST}" "mkdir -p ${REMOTE_DIR}"
ssh "${DEPLOY_USER}@${DEPLOY_HOST}" "mkdir -p ${REMOTE_DIR}/backend ${REMOTE_DIR}/frontend"
scp docker-compose.yml "${DEPLOY_USER}@${DEPLOY_HOST}:${REMOTE_DIR}/"
scp backend/Dockerfile backend/requirements.txt backend/calculadora.py "${DEPLOY_USER}@${DEPLOY_HOST}:${REMOTE_DIR}/backend/"
scp frontend/Dockerfile frontend/index.html frontend/nginx.conf frontend/entrypoint.sh "${DEPLOY_USER}@${DEPLOY_HOST}:${REMOTE_DIR}/frontend/"
ssh "${DEPLOY_USER}@${DEPLOY_HOST}" "cd ${REMOTE_DIR} && docker compose up -d --build"
ssh "${DEPLOY_USER}@${DEPLOY_HOST}" "curl --fail --silent http://localhost:5000/health"

echo "Deployment completed on ${DEPLOY_HOST}"