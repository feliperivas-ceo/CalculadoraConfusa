#!/bin/sh
set -eu

printf 'window.BACKEND_URL = "%s";\n' "$(printf '%s' "${BACKEND_URL:-http://localhost:5000}" | sed 's/[\\&/]/\\&/g; s/"/\\"/g')" \
    > /usr/share/nginx/html/config.js