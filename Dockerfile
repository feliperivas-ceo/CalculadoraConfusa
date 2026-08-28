# Dockerfile - Containerización de Calculadora Confusa (Bonus: Docker)
# Uso:
#   docker build -t calculadora-confusa .
#   docker run -p 5000:5000 calculadora-confusa

FROM python:3.11-slim

# Metadatos
LABEL maintainer="ICESI DevOps"
LABEL description="Calculadora Confusa - Taller DevOps"
LABEL version="1.0"

# Configurar directorio de trabajo
WORKDIR /app

# Establecer variables de entorno
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    FLASK_APP=calculadora.py \
    FLASK_ENV=production

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copiar archivos de dependencias
COPY requirements.txt .

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar aplicación
COPY calculadora.py .
COPY templates/ templates/

# Crear directorio para persistencia
RUN mkdir -p /app/data && \
    echo "[]" > /app/data/historial.json

# Volumen para persistencia (opcional)
VOLUME /app/data

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://127.0.0.1:5000/health || exit 1

# Exponer puerto
EXPOSE 5000

# Comando de inicio
CMD ["python", "calculadora.py"]
