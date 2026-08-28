# Guía Fase 2: DevOps Integrado y Continuous Delivery

## 📅 Duración: 40-50 minutos (Dividido en dos partes)

### Parte 1: Migración con Automatización (15 minutos)

**Objetivo:** Desplegar HU1-3 en servidor limpio usando SOLO scripts automáticos.

#### Pasos en Servidor Ops:

1. **Limpiar ambiente anterior**
   ```bash
   rm -rf .venv historial.json calculadora.log
   ```

2. **Ejecutar script de despliegue**
   ```bash
   # Linux/macOS
   bash deploy.sh
   
   # Windows
   powershell -ExecutionPolicy Bypass -File .\deploy.ps1
   ```

3. **Configurar firewall**
   ```bash
   # Linux/macOS (requiere sudo)
   sudo bash firewall-config.sh
   
   # Windows (requiere admin)
   powershell -ExecutionPolicy Bypass -RunAs Administrator -File .\firewall-config.ps1
   ```

4. **Iniciar aplicación**
   ```bash
   source .venv/bin/activate  # o .\.venv\Scripts\Activate.ps1
   python calculadora.py
   ```

#### Validación (Equipo Dev + Ops):
- [ ] Backend responde en `http://<IP_OPS>:5000`
- [ ] Health check funciona: `curl http://<IP_OPS>:5000/health`
- [ ] Historial vacío correcto: `curl http://<IP_OPS>:5000/historial`
- [ ] Interfaz web carga sin errores

**⏱️ Penalización:** +3 minutos por intento de validación fallido

---

### Parte 2: Desarrollo Continuo (25 minutos)

Con el pipeline en funcionamiento, el equipo recibe las nuevas HUs:

#### HU4: División con Validación
- ✅ Endpoint `/divide` ya implementado
- ✅ Validación de división por cero
- **Tarea Dev:** Validar en interfaz web
- **Tarea Ops:** Monitorear logs

**Pruebas rápidas:**
```bash
# Éxito
curl -X POST -H "Content-Type: application/json" \
  -d '{"num1": "4", "num2": "2"}' \
  http://<IP_OPS>:5000/divide

# Error esperado (division by zero)
curl -X POST -H "Content-Type: application/json" \
  -d '{"num1": "4", "num2": "0"}' \
  http://<IP_OPS>:5000/divide
```

#### HU5: Telemetría y Health Check
- ✅ Endpoints `/health` y `/status` implementados
- **Tarea Dev:** Mostrar dashboard con status
- **Tarea Ops:** Implementar monitoreo continuo

**Endpoints disponibles:**
```bash
# Health del Backend
curl http://<IP_OPS>:5000/health

# Estado general del sistema
curl http://<IP_OPS>:5000/status
```

---

## 🔄 Flujo de Despliegue Continuo (Fase 2)

```
[Dev escribe código]
        ↓
[Commit a rama feature]
        ↓
[Ejecutar deploy.sh en Ops]
        ↓
[Ejecutar pruebas automáticas]
        ↓
[Verificar health check]
        ↓
[Validar en producción]
        ↓
✓ Operación completada
```

---

## 📊 Checklist de Calidad

Antes de dar por completada cada HU, verifica:

### Backend
- [ ] API responde con código HTTP correcto
- [ ] Errores retornan JSON con campo `error` y código 400
- [ ] Health check disponible
- [ ] Logs se escriben en `calculadora.log`
- [ ] Historial se persiste en `historial.json`

### Frontend
- [ ] Interfaz carga sin errores
- [ ] Todos los campos se validan
- [ ] Resultados se muestran correctamente
- [ ] Historial se actualiza en tiempo real
- [ ] Status del backend se indica visualmente

### Infraestructura (Ops)
- [ ] Puerto 5000 abierto en firewall
- [ ] Acceso desde máquina remota confirmado
- [ ] Logs de aplicación son accesibles
- [ ] Permisos de archivo en `historial.json` correctos
- [ ] Uptime de aplicación monitoreado

---

## ⏱️ Métricas a Medir

### Lead Time (Total Fase 2)
- Inicio: Recepción de HU4-5
- Fin: Validación en producción de última HU
- **Meta:** < 40 minutos

### Deployment Frequency
- **Fase 1:** HU1, HU2, HU3 (3 despliegues)
- **Fase 2:** HU4 + HU5 (2 despliegues adicionales)
- **Total:** 5 despliegues

### Change Failure Rate
- Fallos = intentos de validación que no funcionan
- Cálculo: Fallos / Total intentos × 100
- **Meta:** < 20%

---

## 🚨 Problemas Comunes y Soluciones

| Problema | Causa | Solución |
|----------|-------|----------|
| Puerto 5000 ya en uso | Proceso anterior no terminó | `killall python` o reiniciar |
| Acceso remoto denegado | Firewall bloqueando | Ejecutar `firewall-config.sh/ps1` nuevamente |
| Import flask_cors error | Dependencia no instalada | Re-ejecutar `deploy.sh/ps1` |
| Historial.json no se actualiza | Permisos incorrectos | Verificar propietario del archivo |
| Health check retorna error | Backend detenido | Asegurar que `python calculadora.py` corre |

---

## 💡 Tips para Fase 2

1. **Parallelización:** Dev y Ops pueden trabajar simultáneamente
   - Dev: Codifica cambios
   - Ops: Monitorea infraestructura

2. **Comunicación integrada:** Usa mensajes síncronos
   - Slack, Microsoft Teams, o comunicación directa

3. **Automatización máxima:** Todo debe ser script
   - Evita pasos manuales repetitivos
   - Documenta comandos en archivos `.sh` o `.ps1`

4. **Testing rápido:** Valida con curl antes de UI
   - Más rápido que abrir navegador
   - Fácil de automatizar

---

## 📋 Tabla de Responsabilidades Compartidas

| Tarea | Dev | Ops | Ambos |
|-------|-----|-----|-------|
| Escribir código | ✅ |  | ✓ Review |
| Ejecutar deploy | | ✅ | ✓ Validar |
| Monitorear logs | ✓ | ✅ | ✓ Analizar |
| Configurar firewall | | ✅ |  |
| Probar APIs | | | ✅ |
| Retroalimentación | ✓ | ✅ | ✓ Feedback |

---

**Fin de Fase 2 = Fin del Taller** ✓

*Reflexión posterior: ¿Cómo fue la comunicación? ¿Qué mejoraría en un escenario real?*
