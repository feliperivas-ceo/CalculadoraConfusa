FROM python:3.11-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    FLASK_APP=backend/calculadora.py \
    FLASK_ENV=production \
    HISTORIAL_FILE=/app/data/historial.json

RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

COPY backend/requirements.txt backend/requirements.txt
RUN pip install --no-cache-dir -r backend/requirements.txt

COPY backend/ backend/
RUN mkdir -p /app/data \
    && test -f /app/data/historial.json || echo "[]" > /app/data/historial.json

VOLUME ["/app/data"]
EXPOSE 5000

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://127.0.0.1:5000/health || exit 1

CMD ["python", "backend/calculadora.py"]