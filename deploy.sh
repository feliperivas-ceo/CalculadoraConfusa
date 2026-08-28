#!/bin/bash

###############################################################################
# deploy.sh - Script de Despliegue Automatizado (Fase 2: DevOps)
# Descripción: Instala dependencias y despliega la aplicación Calculadora Confusa
# Uso: bash deploy.sh
###############################################################################

set -e  # Exit on error

echo "=========================================="
echo "Calculadora Confusa - Script de Despliegue"
echo "=========================================="
echo ""

# Detectar SO
if [[ "$OSTYPE" == "darwin"* ]]; then
    PYTHON_CMD="python3"
    echo "✓ Detectado: macOS"
elif [[ "$OSTYPE" == "linux"* ]]; then
    PYTHON_CMD="python3"
    echo "✓ Detectado: Linux"
else
    echo "❌ Sistema operativo no soportado por este script"
    exit 1
fi

# Paso 1: Verificar Python
echo ""
echo "[1/5] Verificando Python..."
if ! command -v $PYTHON_CMD &> /dev/null; then
    echo "❌ Python 3 no está instalado"
    exit 1
fi
PYTHON_VERSION=$($PYTHON_CMD --version | awk '{print $2}')
echo "✓ Python $PYTHON_VERSION encontrado"

# Paso 2: Crear/Activar entorno virtual
echo ""
echo "[2/5] Configurando entorno virtual..."
if [ ! -d ".venv" ]; then
    $PYTHON_CMD -m venv .venv
    echo "✓ Entorno virtual creado"
else
    echo "✓ Entorno virtual ya existe"
fi

# Activar entorno virtual
if [[ "$OSTYPE" == "darwin"* ]] || [[ "$OSTYPE" == "linux"* ]]; then
    source .venv/bin/activate
fi

# Paso 3: Instalar/Actualizar dependencias
echo ""
echo "[3/5] Instalando dependencias..."
.venv/bin/pip install --upgrade pip > /dev/null 2>&1
.venv/bin/pip install -r requirements.txt
echo "✓ Dependencias instaladas"

# Paso 4: Verificar estructura de directorios
echo ""
echo "[4/5] Verificando estructura de archivos..."
if [ ! -f "calculadora.py" ]; then
    echo "❌ No se encontró calculadora.py"
    exit 1
fi
if [ ! -d "templates" ]; then
    echo "❌ No se encontró el directorio templates"
    exit 1
fi
if [ ! -f "templates/index.html" ]; then
    echo "❌ No se encontró templates/index.html"
    exit 1
fi
echo "✓ Estructura de archivos correcta"

# Paso 5: Crear archivo de historial vacío si no existe
echo ""
echo "[5/5] Inicializando sistema de persistencia..."
if [ ! -f "historial.json" ]; then
    echo "[]" > historial.json
    echo "✓ Archivo de historial inicializado"
else
    echo "✓ Historial existente"
fi

echo ""
echo "=========================================="
echo "✓ Despliegue completado exitosamente"
echo "=========================================="
echo ""
echo "Para ejecutar la aplicación:"
echo "  source .venv/bin/activate"
echo "  python calculadora.py"
echo ""
echo "Luego abre en tu navegador:"
echo "  http://127.0.0.1:5000"
echo ""
