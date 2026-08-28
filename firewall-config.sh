#!/bin/bash

###############################################################################
# firewall-config.sh - Script de Configuración de Firewall (Fase 2: DevOps)
# Descripción: Abre puertos necesarios en el firewall para la aplicación
# Uso: sudo bash firewall-config.sh
# Nota: Requiere permisos de administrador (sudo)
###############################################################################

set -e

echo "=========================================="
echo "Configuración de Firewall - Calculadora Confusa"
echo "=========================================="
echo ""

# Verificar si se ejecuta como root
if [[ $EUID -ne 0 ]]; then
   echo "❌ Este script debe ejecutarse con permisos de administrador (sudo)"
   exit 1
fi

# Detectar sistema y gestor de firewall
if command -v ufw &> /dev/null; then
    FIREWALL="ufw"
    echo "✓ Detectado: UFW (Ubuntu/Debian)"
elif command -v firewalld &> /dev/null; then
    FIREWALL="firewalld"
    echo "✓ Detectado: Firewalld (CentOS/RHEL)"
else
    echo "❌ No se detectó UFW ni Firewalld"
    echo "Por favor, configura manualmente el puerto 5000"
    exit 1
fi

echo ""

# Configuración según tipo de firewall
if [ "$FIREWALL" == "ufw" ]; then
    echo "[1/3] Habilitando UFW..."
    ufw --force enable > /dev/null 2>&1 || true
    echo "✓ UFW habilitado"
    
    echo "[2/3] Abriendo puerto 5000 (Backend)..."
    ufw allow 5000/tcp > /dev/null 2>&1
    echo "✓ Puerto 5000 abierto para TCP"
    
    echo "[3/3] Mostrando estado actual..."
    echo ""
    ufw status
    
elif [ "$FIREWALL" == "firewalld" ]; then
    echo "[1/3] Iniciando Firewalld..."
    systemctl start firewalld > /dev/null 2>&1 || true
    systemctl enable firewalld > /dev/null 2>&1 || true
    echo "✓ Firewalld iniciado"
    
    echo "[2/3] Abriendo puerto 5000 (Backend)..."
    firewall-cmd --permanent --add-port=5000/tcp > /dev/null 2>&1
    firewall-cmd --reload > /dev/null 2>&1
    echo "✓ Puerto 5000 abierto para TCP"
    
    echo "[3/3] Mostrando estado actual..."
    echo ""
    firewall-cmd --list-ports
fi

echo ""
echo "=========================================="
echo "✓ Configuración de firewall completada"
echo "=========================================="
echo ""
echo "La aplicación Backend estará disponible en:"
echo "  http://127.0.0.1:5000"
echo ""
echo "Desde otra máquina (reemplaza 127.0.0.1 con la IP de este servidor):"
echo "  http://<IP_DEL_SERVIDOR>:5000"
echo ""
