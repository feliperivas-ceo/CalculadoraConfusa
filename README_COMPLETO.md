# Calculadora Confusa 🧮 — Taller DevOps ICESI

> Simulación de Despliegue DevOps: La Pared de la Confusión y Automatización

Esta es una aplicación web educativa que implementa **todas las Historias de Usuario (HU1-HU5)** para el Taller 2 de Ingeniería de Software V en la Universidad ICESI.

## ✨ Características Implementadas

### ✅ HU1: Servicio de Suma (Backend y Frontend)
- Endpoint `POST /suma` en backend
- Frontend interactivo para entrada de datos
- Soporta números enteros, decimales y fracciones
- Retorna resultado en formato fraccionario y decimal

### ✅ HU2: Multi-Operación (Resta y Multiplicación)
- Endpoint `POST /resta` 
- Endpoint `POST /multiplica`
- Selector visual de operaciones en interfaz
- Misma funcionalidad de parseo de fracciones

### ✅ HU3: Historial del Sistema de Registro (SoR)
- Persistencia en archivo JSON local (`historial.json`)
- Endpoint `GET /historial` para consultar últimas 5 operaciones
- Visualización de historial en interfaz web
- Registro automático de operaciones exitosas
- Logging estructurado a archivo `calculadora.log`

### ✅ HU4: División con Validación
- Endpoint `POST /divide`
- Validación de división por cero (retorna HTTP 400)
- Manejo robusto de errores
- Logging de intentos de división por cero

### ✅ HU5: Telemetría y Health Check
- Endpoint `GET /health` — estado de salud del Backend
  - Retorna: estado, uptime, permisos de persistencia
- Endpoint `GET /status` — estado general de la aplicación
  - Retorna: estado operacional, versión, uptime en segundos, operaciones registradas
- Indicador visual en UI del estado del backend
- Badge de versión (v1.0 HU1-5)

## 📋 Estructura del Proyecto

```
CalculadoraConfusa/
├── backend/
│   ├── calculadora.py          # Backend Flask (HU1-HU5)
│   ├── requirements.txt        # Dependencias Python
│   └── test_calculadora.py     # Pruebas de endpoints
├── historial.json             # Persistencia de operaciones
├── calculadora.log            # Log de operaciones
├── frontend/
│   ├── index.html              # Frontend interactivo
│   ├── Dockerfile              # Imagen Nginx
│   ├── nginx.conf              # Servidor de archivos estáticos
│   └── entrypoint.sh           # Configuración de URL del backend
├── scripts/
│   ├── test_endpoints.sh       # Pruebas para CI
│   └── deploy.sh               # Despliegue remoto por SSH
├── docker-compose.yml          # Orquestación de ambos servicios
├── .github/workflows/ci.yml   # Pipeline de integración continua
├── .dockerignore               # Contexto de build mínimo
├── HU.md                      # Especificación del taller
└── README.md                  # Este archivo
```

## 🚀 Guía de Despliegue

### Ejecución local

#### 1. Preparar el Entorno

```bash
# Crear entorno virtual
python -m venv .venv

# Activar entorno (Linux/macOS)
source .venv/bin/activate

# Activar entorno (Windows PowerShell)
.\.venv\Scripts\Activate.ps1

# Instalar dependencias
pip install -r backend/requirements.txt
```

#### 2. Ejecutar el backend

```bash
python backend/calculadora.py
```

La aplicación estará disponible en:
- **Backend:** http://127.0.0.1:5000
- **APIs REST:** http://127.0.0.1:5000/suma, /resta, /multiplica, /divide

Para levantar los dos contenedores de forma conjunta:

```bash
docker compose up -d --build
```

- **Frontend:** http://127.0.0.1:8080
- **Backend:** http://127.0.0.1:5000

La URL que usará el frontend puede cambiarse con `BACKEND_URL`:

```bash
BACKEND_URL=http://192.168.1.20:5000 docker compose up -d --build
```

Para ejecutar el backend en una PC y el frontend en otra, levanta primero el backend
en la PC servidora. El backend escucha en la red local mediante `FLASK_HOST=0.0.0.0`.
Después, desde la PC del frontend, despliega únicamente su contenedor por SSH:

```bash
FRONTEND_HOST=192.168.131.37 \
FRONTEND_USER=usuario_ssh \
BACKEND_URL=http://192.168.131.192:5000 \
bash scripts/deploy-frontend.sh
```

El frontend remoto quedará disponible en `http://192.168.131.37:8080`.

#### 3. Pruebas de Endpoints

```bash
# Suma (HU1)
curl -X POST -H "Content-Type: application/json" \
  -d '{"num1": "1/2", "num2": "3/4"}' \
  http://127.0.0.1:5000/suma

# Respuesta esperada:
# {"decimal":1.25,"resultado":"5/4","resultado_formateado":"5/4 (1.25)","status":"success"}

# Resta (HU2)
curl -X POST -H "Content-Type: application/json" \
  -d '{"num1": "1.5", "num2": "3/4"}' \
  http://127.0.0.1:5000/resta

# Multiplicación (HU2)
curl -X POST -H "Content-Type: application/json" \
  -d '{"num1": "2/3", "num2": "3/4"}' \
  http://127.0.0.1:5000/multiplica

# División (HU4) - Éxito
curl -X POST -H "Content-Type: application/json" \
  -d '{"num1": "1", "num2": "2"}' \
  http://127.0.0.1:5000/divide

# División por cero (HU4) - Error esperado
curl -X POST -H "Content-Type: application/json" \
  -d '{"num1": "5", "num2": "0"}' \
  http://127.0.0.1:5000/divide

# Historial (HU3)
curl http://127.0.0.1:5000/historial

# Health Check (HU5)
curl http://127.0.0.1:5000/health

# Status (HU5)
curl http://127.0.0.1:5000/status
```

---

### Integración continua y despliegue SSH

El workflow [ci.yml](.github/workflows/ci.yml) construye ambas imágenes y ejecuta las pruebas de endpoints en cada `push` o `pull_request` hacia `main`.

Para desplegar en el equipo asignado, configure una llave SSH y ejecute en Linux/macOS:

**En Linux/macOS:**
```bash
DEPLOY_HOST=192.168.1.30 DEPLOY_USER=estudiante bash scripts/deploy.sh
```

En Windows PowerShell, use el script equivalente:

```powershell
.\scripts\deploy-frontend.ps1 `
  -FrontendHost 192.168.131.37 `
  -FrontendUser swarch `
  -BackendUrl http://192.168.131.192:5000
```

El destino debe tener Docker y Docker Compose instalados. Para la validación cruzada:

En la PC del **Frontend**, accede al Backend del servidor Ops:
```bash
# Reemplaza <IP_BACKEND> con la IP real del servidor Ops
curl http://<IP_BACKEND>:5000/health
```

En el navegador del **Frontend**:
```
http://<IP_BACKEND>:5000
```

---

## 📊 Métricas DevOps a Medir

- **Lead Time:** Tiempo desde solicitud de HU hasta validación en producción
- **Deployment Frequency:** Número de HUs completadas por fase (Objetivo: HU1-3 en Fase 1, HU4-5 en Fase 2)
- **Change Failure Rate:** Fallos en validación / total intentos
  - Penalización: +3 minutos por fallo

---

## 🔍 Monitoreo y Logs

### Logs de Aplicación

El archivo `calculadora.log` registra:
- Operaciones exitosas
- Errores de entrada
- Intento de división por cero
- Health checks
- Cambios en historial

**Ver logs:**
```bash
# Linux/macOS
tail -f calculadora.log

# Windows PowerShell
Get-Content calculadora.log -Wait
```

### Archivos de Persistencia

- **historial.json:** Últimas 5 operaciones en formato JSON
  - Se actualiza automáticamente tras cada operación
  - Estructura: `[{"timestamp", "num1", "num2", "operacion", "resultado"}]`

---

## 🛠️ Troubleshooting

### Puerto 5000 en uso
```bash
# Linux/macOS: Encontrar proceso
lsof -i :5000

# Windows PowerShell:
Get-NetTCPConnection -LocalPort 5000 -ErrorAction SilentlyContinue
```

### Problema de permisos en firewall
- **Linux:** Asegúrate de usar `sudo` para `firewall-config.sh`
- **Windows:** Ejecuta PowerShell como administrador

### Falta flask-cors
```bash
pip install flask-cors
```

### Problemas de acceso remoto (Fase 2)
1. Verifica que el firewall esté correctamente configurado
2. Confirma la IP del servidor: `ipconfig` (Windows) o `ifconfig` (Linux/macOS)
3. Usa esa IP en el cliente: `http://<IP>:5000`

---

## 📚 Recursos Educativos

- **HU.md:** Especificación completa del taller y objetivos de aprendizaje
- **Backend (backend/calculadora.py):** Implementación de APIs REST, manejo de errores, logging
- **Frontend (frontend/index.html):** UI responsiva, manejo de formularios
- **Scripts:** Automatización de despliegue, gestión de firewall

---

## 👥 Roles de Equipo (Simulación)

| Rol | Responsabilidades |
|-----|-------------------|
| **Desarrolladores (Dev)** | Codificar HUs, crear APIs REST, pruebas unitarias |
| **DevOps (Ops)** | Despliegue, firewall, monitoring, infraestructura |

**Fase 1:** Equipos separados con comunicación asincrónica  
**Fase 2:** Equipos integrados con responsabilidad compartida

---

## 📝 Notas Importantes

- ✅ **Debug mode desactivado** para seguridad en producción
- ✅ **CORS habilitado** para acceso desde diferentes orígenes
- ✅ **Logging estructurado** a archivo local
- ✅ **Validación robusta** de entrada de usuario
- ⚠️ Para producción: configurar secret key, usar DB externa, SSL/TLS

---

## 📄 Licencia

Proyecto educativo — Universidad ICESI

---

**Última actualización:** Agosto 2026  
**Versión:** 1.0 (HU1-5 Completas)
