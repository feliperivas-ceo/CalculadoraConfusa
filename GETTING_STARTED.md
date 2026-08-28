# 🚀 INICIO RÁPIDO - Calculadora Confusa

## ¿Qué es esto?

Un proyecto educativo de **Ingeniería de Software V** que simula el despliegue real de una aplicación web, experimentando:
- ❌ Fricción de **equipos en silos** (Fase 1)
- ✅ Automatización y **DevOps integrado** (Fase 2)

---

## ⚡ Empezar en 2 Minutos

### Windows (PowerShell)

```powershell
# 1. Instalar dependencias automáticamente
powershell -ExecutionPolicy Bypass -File .\deploy.ps1

# 2. Activar entorno
.\.venv\Scripts\Activate.ps1

# 3. Ejecutar
python calculadora.py
```

### Linux / macOS (Bash)

```bash
# 1. Instalar dependencias automáticamente
bash deploy.sh

# 2. Activar entorno
source .venv/bin/activate

# 3. Ejecutar
python calculadora.py
```

---

## 🌐 Acceder a la Aplicación

Abre tu navegador en:
👉 **http://127.0.0.1:5000**

---

## 🧪 Validar Que Todo Funciona

```bash
# Instalar herramienta de testing
pip install requests

# Ejecutar suite de pruebas
python test_calculadora.py
```

Deberías ver ✅ en todas las pruebas.

---

## 📚 Documentación

| Archivo | Propósito |
|---------|-----------|
| **README_COMPLETO.md** | Guía detallada de todas las features |
| **FASE2_GUIA.md** | Instrucciones para Fase 2 (DevOps) |
| **RESUMEN_CAMBIOS.md** | Qué se implementó y por qué |
| **HU.md** | Especificación original del taller |

---

## 🎯 ¿Qué Contiene?

### Implementado ✅

- **HU1:** Suma de números (fracciones, decimales, enteros)
- **HU2:** Resta y multiplicación
- **HU3:** Historial de operaciones (persistencia)
- **HU4:** División con validación (error por cero)
- **HU5:** Health check y telemetría

### Tecnología

- Backend: **Python + Flask**
- Frontend: **HTML/CSS/JavaScript** (responsive)
- Persistencia: **JSON local** + Logging
- Automatización: **Scripts Bash + PowerShell**

---

## 🔧 Troubleshooting

### ❌ "Port 5000 already in use"
```bash
# Encontrar proceso
lsof -i :5000           # macOS/Linux
Get-NetTCPConnection -LocalPort 5000  # Windows

# Matar proceso
kill -9 <PID>           # macOS/Linux
taskkill /PID <PID> /F  # Windows
```

### ❌ "ModuleNotFoundError: No module named 'flask'"
```bash
pip install -r requirements.txt
```

### ❌ "Firewall blocking port"
```bash
# Linux
sudo bash firewall-config.sh

# Windows (como admin)
powershell -RunAs Administrator -File .\firewall-config.ps1
```

---

## 📊 Próximos Pasos

### Fase 1: Ejecutar Manualmente (35-40 min)
1. ✅ Hacer suma, resta, multiplicación
2. ✅ Ver historial guardarse
3. ✅ Probar que el frontend funcione en una PC y backend en otra

### Fase 2: Automatizar (40-50 min)
1. ✅ Usar script `deploy.sh` o `deploy.ps1`
2. ✅ Configurar firewall con `firewall-config.sh` o `.ps1`
3. ✅ Probar división e implementar health check
4. ✅ Medir Lead Time, Deployment Frequency, Failure Rate

---

## 🐳 Bonus: Docker

```bash
# Instalar Docker Desktop (si no tienes)

# Ejecutar con Docker Compose
docker-compose up

# Acceder a http://localhost:5000
```

---

## 💬 Preguntas Frecuentes

**P: ¿Puedo acceder desde otra PC?**  
R: Sí, reemplaza `127.0.0.1` con la IP del servidor: `http://<IP>:5000`

**P: ¿Dónde se guardan las operaciones?**  
R: En `historial.json` (último 5 operaciones) y logs en `calculadora.log`

**P: ¿Es production-ready?**  
R: No, es educativo. Para producción: agregar DB, SSL/TLS, auth, etc.

**P: ¿Puedo modificar el código?**  
R: ¡Sí! Experimenta con cambios y observa cómo afecta el Lead Time

---

## 🎓 Lo Que Aprenderás

✨ Cómo funciona DevOps en la práctica  
✨ Por qué la automatización reduce fricción  
✨ Cómo medir la efectividad de cambios  
✨ Configuración básica de firewall  
✨ Despliegue y monitoreo de aplicaciones  

---

## ✅ Checklist de Validación

- [ ] Página de inicio carga (http://127.0.0.1:5000)
- [ ] Suma: `1/2 + 3/4 = 5/4`
- [ ] Resta: `1.5 - 0.75 = 0.75`
- [ ] Multiplicación: `2/3 × 3/4 = 1/2`
- [ ] División: `4 ÷ 2 = 2`
- [ ] División por cero: retorna error
- [ ] Historial muestra últimas 5 operaciones
- [ ] Health check: `curl http://127.0.0.1:5000/health`
- [ ] Status: `curl http://127.0.0.1:5000/status`

---

## 🏆 ¡Listo para Fase 2!

Si todo funciona, estás listo para:

1. **Limpiar el ambiente**
2. **Ejecutar scripts automáticos** en servidores separados
3. **Medir métricas** de Lead Time y Failure Rate
4. **Implementar HU4 y HU5**
5. **Experimentar DevOps integrado**

---

**Última ayuda:** Revisa `README_COMPLETO.md` para guía detallada.

**¡Buena suerte! 🚀**
