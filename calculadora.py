from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from fractions import Fraction
import json
import os
import logging
from datetime import datetime, timedelta
import time

app = Flask(__name__)
CORS(app)

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('calculadora.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Constants
HISTORIAL_FILE = "historial.json"
MAX_HISTORIAL = 5
START_TIME = time.time()

def load_historial():
    """Carga el historial de operaciones desde archivo JSON."""
    if os.path.exists(HISTORIAL_FILE):
        try:
            with open(HISTORIAL_FILE, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error al cargar historial: {e}")
            return []
    return []

def save_historial(historial):
    """Guarda el historial de operaciones en archivo JSON."""
    try:
        with open(HISTORIAL_FILE, 'w') as f:
            json.dump(historial, f, indent=2)
        logger.info(f"Historial guardado: {len(historial)} operaciones")
    except Exception as e:
        logger.error(f"Error al guardar historial: {e}")

def add_to_historial(num1, num2, operacion, resultado):
    """Añade una operación exitosa al historial."""
    historial = load_historial()
    entry = {
        "timestamp": datetime.now().isoformat(),
        "num1": num1,
        "num2": num2,
        "operacion": operacion,
        "resultado": resultado
    }
    historial.insert(0, entry)
    historial = historial[:MAX_HISTORIAL]
    save_historial(historial)
    logger.info(f"Operación registrada: {operacion}({num1}, {num2}) = {resultado}")
    return historial

def parse_fraction(val_str):
    """Parses a string into a Fraction. Supports integers, decimals, and 'a/b' fractions."""
    if not val_str:
        raise ValueError("El campo está vacío")
    val_str = val_str.strip().replace(" ", "")
    try:
        return Fraction(val_str)
    except (ValueError, ZeroDivisionError) as e:
        raise ValueError(f"Valor inválido '{val_str}': Debe ser entero, decimal o fracción (ej: 1/2)")

def format_result(frac):
    """Formats a Fraction object to a nice string showing both fraction and decimal representation."""
    if frac.denominator == 1:
        return f"{frac.numerator}"
    dec_val = float(frac)
    return f"{frac.numerator}/{frac.denominator} ({dec_val})"

# ============ HU1 & HU2: Operaciones Básicas (Suma, Resta, Multiplicación) ============

@app.route("/suma", methods=["POST"])
def api_suma():
    """HU1: Suma de dos números"""
    try:
        data = request.get_json(silent=True) or request.form
        num1_str = data.get("num1", "").strip()
        num2_str = data.get("num2", "").strip()
        
        n1 = parse_fraction(num1_str)
        n2 = parse_fraction(num2_str)
        res = n1 + n2
        
        resultado_formateado = format_result(res)
        add_to_historial(num1_str, num2_str, "suma", resultado_formateado)
        
        return jsonify({
            "resultado": str(res),
            "resultado_formateado": resultado_formateado,
            "decimal": float(res),
            "status": "success"
        })
    except ValueError as e:
        logger.warning(f"Error en suma: {e}")
        return jsonify({"error": str(e), "status": "error"}), 400

@app.route("/resta", methods=["POST"])
def api_resta():
    """HU2: Resta de dos números"""
    try:
        data = request.get_json(silent=True) or request.form
        num1_str = data.get("num1", "").strip()
        num2_str = data.get("num2", "").strip()
        
        n1 = parse_fraction(num1_str)
        n2 = parse_fraction(num2_str)
        res = n1 - n2
        
        resultado_formateado = format_result(res)
        add_to_historial(num1_str, num2_str, "resta", resultado_formateado)
        
        return jsonify({
            "resultado": str(res),
            "resultado_formateado": resultado_formateado,
            "decimal": float(res),
            "status": "success"
        })
    except ValueError as e:
        logger.warning(f"Error en resta: {e}")
        return jsonify({"error": str(e), "status": "error"}), 400

@app.route("/multiplica", methods=["POST"])
def api_multiplica():
    """HU2: Multiplicación de dos números"""
    try:
        data = request.get_json(silent=True) or request.form
        num1_str = data.get("num1", "").strip()
        num2_str = data.get("num2", "").strip()
        
        n1 = parse_fraction(num1_str)
        n2 = parse_fraction(num2_str)
        res = n1 * n2
        
        resultado_formateado = format_result(res)
        add_to_historial(num1_str, num2_str, "multiplica", resultado_formateado)
        
        return jsonify({
            "resultado": str(res),
            "resultado_formateado": resultado_formateado,
            "decimal": float(res),
            "status": "success"
        })
    except ValueError as e:
        logger.warning(f"Error en multiplicación: {e}")
        return jsonify({"error": str(e), "status": "error"}), 400

# ============ HU4: División con Validación ============

@app.route("/divide", methods=["POST"])
def api_divide():
    """HU4: División de dos números con validación de cero"""
    try:
        data = request.get_json(silent=True) or request.form
        num1_str = data.get("num1", "").strip()
        num2_str = data.get("num2", "").strip()
        
        n1 = parse_fraction(num1_str)
        n2 = parse_fraction(num2_str)
        
        # Validación de división por cero
        if n2 == 0:
            error_msg = "Error: División por cero no permitida"
            logger.error(f"Intento de división por cero: {num1_str} / {num2_str}")
            return jsonify({"error": error_msg, "status": "error"}), 400
        
        res = n1 / n2
        
        resultado_formateado = format_result(res)
        add_to_historial(num1_str, num2_str, "divide", resultado_formateado)
        
        return jsonify({
            "resultado": str(res),
            "resultado_formateado": resultado_formateado,
            "decimal": float(res),
            "status": "success"
        })
    except ValueError as e:
        logger.warning(f"Error en división: {e}")
        return jsonify({"error": str(e), "status": "error"}), 400

# ============ HU3: Sistema de Registro (Historial) ============

@app.route("/historial", methods=["GET"])
def api_historial():
    """HU3: Obtiene el historial de últimas operaciones exitosas"""
    try:
        historial = load_historial()
        logger.info(f"Historial consultado: {len(historial)} operaciones")
        return jsonify({
            "historial": historial,
            "total": len(historial),
            "status": "success"
        })
    except Exception as e:
        logger.error(f"Error al obtener historial: {e}")
        return jsonify({"error": str(e), "status": "error"}), 500

# ============ HU5: Telemetría y Health Check ============

@app.route("/health", methods=["GET"])
def health_check():
    """HU5: Endpoint de salud del Backend"""
    try:
        # Verificar acceso a archivo de historial
        can_write = os.access(os.path.dirname(HISTORIAL_FILE) or ".", os.W_OK)
        uptime_seconds = time.time() - START_TIME
        uptime = str(timedelta(seconds=int(uptime_seconds)))
        
        logger.info("Health check ejecutado")
        return jsonify({
            "status": "healthy",
            "service": "Calculadora Backend",
            "uptime": uptime,
            "uptime_seconds": int(uptime_seconds),
            "persistence": "enabled" if can_write else "disabled",
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"Error en health check: {e}")
        return jsonify({"status": "unhealthy", "error": str(e)}), 500

@app.route("/status", methods=["GET"])
def status_endpoint():
    """HU5: Endpoint de estado general de la aplicación"""
    try:
        historial = load_historial()
        can_write = os.access(os.path.dirname(HISTORIAL_FILE) or ".", os.W_OK)
        uptime_seconds = time.time() - START_TIME
        
        logger.info("Status endpoint consultado")
        return jsonify({
            "status": "operational",
            "service": "Calculadora DevOps",
            "version": "1.0",
            "uptime_seconds": int(uptime_seconds),
            "operations_logged": len(historial),
            "persistence_writable": can_write,
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"Error en status endpoint: {e}")
        return jsonify({"status": "error", "error": str(e)}), 500

# ============ UI Controller Route ============

@app.route("/", methods=["GET", "POST"])
def calcular():
    """Interfaz web interactiva"""
    resultado = None
    historial = load_historial()
    num1_raw = ""
    num2_raw = ""
    operacion = "suma"
    error = None
    
    if request.method == "POST":
        num1_raw = request.form.get("num1", "").strip()
        num2_raw = request.form.get("num2", "").strip()
        operacion = request.form.get("operacion", "suma")
        
        try:
            n1 = parse_fraction(num1_raw)
            n2 = parse_fraction(num2_raw)
            
            if operacion == "suma":
                res = n1 + n2
            elif operacion == "resta":
                res = n1 - n2
            elif operacion == "multiplica":
                res = n1 * n2
            elif operacion == "divide":
                if n2 == 0:
                    raise ValueError("Error: División por cero no permitida")
                res = n1 / n2
            else:
                raise ValueError("Operación no soportada")
            
            resultado = format_result(res)
            add_to_historial(num1_raw, num2_raw, operacion, resultado)
            historial = load_historial()
            
        except ValueError as e:
            error = str(e)
            logger.warning(f"Error en UI: {error}")
    
    return render_template(
        "index.html",
        resultado=resultado,
        error=error,
        num1=num1_raw,
        num2=num2_raw,
        operacion=operacion,
        historial=historial
    )

if __name__ == "__main__":
    logger.info("Iniciando aplicación Calculadora Confusa")
    app.run(host="127.0.0.1", port=5000, debug=False)
