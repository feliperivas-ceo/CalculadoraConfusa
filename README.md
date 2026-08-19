# Calculadora Confusa 🧮

Este proyecto es parte del **Taller 2: Simulación de Despliegue DevOps — La Pared de la Confusión y Automatización**. Consiste en una aplicación web básica construida con Flask para demostrar conceptos de despliegue, comunicación entre silos y automatización.

## Requisitos Previos

- Python 3.x instalado.

## Instrucciones de Instalación y Ejecución

### 1. Preparación del Entorno Virtual

Si aún no has configurado el entorno virtual o instalado las dependencias, ejecuta:

```bash
# Crear el entorno virtual (.venv) en el directorio raíz
python -m venv .venv

# Instalar las dependencias requeridas
./.venv/bin/pip install -r requirements.txt
```

### 2. Ejecutar la Aplicación

Puedes ejecutar el servidor directamente usando el intérprete de Python dentro del entorno virtual:

```bash
./.venv/bin/python calculadora.py
```

#### Alternativa: Activando el entorno virtual

Si prefieres activar el entorno en tu terminal antes de correr la aplicación:

* **En Bash / Zsh:**
  ```bash
  source .venv/bin/activate
  python calculadora.py
  ```

* **En Fish shell:**
  ```fish
  source .venv/bin/activate.fish
  python calculadora.py
  ```

### 3. Acceder a la Aplicación

Una vez que el servidor esté en ejecución, abre tu navegador web e ingresa a:

👉 **[http://127.0.0.1:5000](http://127.0.0.1:5000)**

---

## Pruebas de Endpoints (Fase 1 - HU2)

El backend incorpora endpoints específicos que reciben y retornan JSON (soportando números enteros, decimales y fracciones en formato texto como `1/2`).

### 1. Servicio de Suma (HU1)
```bash
curl -s -X POST -H "Content-Type: application/json" \
  -d '{"num1": "1/2", "num2": "3/4"}' \
  http://127.0.0.1:5000/suma
```
*Respuesta esperada:* `{"decimal":1.25,"resultado":"5/4","resultado_formateado":"5/4 (1.25)"}`

### 2. Servicio de Resta (HU2)
```bash
curl -s -X POST -H "Content-Type: application/json" \
  -d '{"num1": "1.5", "num2": "3/4"}' \
  http://127.0.0.1:5000/resta
```
*Respuesta esperada:* `{"decimal":0.75,"resultado":"3/4","resultado_formateado":"3/4 (0.75)"}`

### 3. Servicio de Multiplicación (HU2)
```bash
curl -s -X POST -H "Content-Type: application/json" \
  -d '{"num1": "2/3", "num2": "3/4"}' \
  http://127.0.0.1:5000/multiplica
```
*Respuesta esperada:* `{"decimal":0.5,"resultado":"1/2","resultado_formateado":"1/2 (0.5)"}`

