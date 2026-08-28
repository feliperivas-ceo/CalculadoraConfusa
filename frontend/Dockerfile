FROM nginx:1.27-alpine

ARG BACKEND_URL=http://localhost:5000
ENV BACKEND_URL=${BACKEND_URL}

COPY frontend/index.html /usr/share/nginx/html/index.html
COPY frontend/nginx.conf /etc/nginx/conf.d/default.conf
COPY frontend/entrypoint.sh /docker-entrypoint.d/40-backend-config.sh

RUN chmod +x /docker-entrypoint.d/40-backend-config.sh

EXPOSE 80