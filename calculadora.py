from flask import Flask, render_template, request, jsonify
from fractions import Fraction

app = Flask(__name__)

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
    
    # Calculate decimal value
    dec_val = float(frac)
    return f"{frac.numerator}/{frac.denominator} ({dec_val})"

# Backend REST Endpoints (HU1 & HU2)

@app.route("/suma", methods=["POST"])
def api_suma():
    try:
        data = request.get_json(silent=True) or request.form
        n1 = parse_fraction(data.get("num1"))
        n2 = parse_fraction(data.get("num2"))
        res = n1 + n2
        return jsonify({
            "resultado": str(res),
            "resultado_formateado": format_result(res),
            "decimal": float(res)
        })
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@app.route("/resta", methods=["POST"])
def api_resta():
    try:
        data = request.get_json(silent=True) or request.form
        n1 = parse_fraction(data.get("num1"))
        n2 = parse_fraction(data.get("num2"))
        res = n1 - n2
        return jsonify({
            "resultado": str(res),
            "resultado_formateado": format_result(res),
            "decimal": float(res)
        })
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@app.route("/multiplica", methods=["POST"])
def api_multiplica():
    try:
        data = request.get_json(silent=True) or request.form
        n1 = parse_fraction(data.get("num1"))
        n2 = parse_fraction(data.get("num2"))
        res = n1 * n2
        return jsonify({
            "resultado": str(res),
            "resultado_formateado": format_result(res),
            "decimal": float(res)
        })
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

# UI Controller Route

@app.route("/", methods=["GET", "POST"])
def calcular():
    resultado = None
    num1_raw = ""
    num2_raw = ""
    operacion = "suma"
    error = None
    
    if request.method == "POST":
        num1_raw = request.form.get("num1", "")
        num2_raw = request.form.get("num2", "")
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
            else:
                raise ValueError("Operación no soportada")
                
            resultado = format_result(res)
        except ValueError as e:
            error = str(e)
        
    return render_template(
        "index.html", 
        resultado=resultado,
        error=error,
        num1=num1_raw,
        num2=num2_raw,
        operacion=operacion
    )

if __name__ == "__main__":
    app.run(debug=True)
