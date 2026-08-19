from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def calcular():
    resultado = None
    
    if request.method == "POST":
        n1 = float(request.form.get("num1", 0))
        n2 = float(request.form.get("num2", 0))
        resultado = n1 + n2  # Tu lógica de negocio
        
    # Flask busca "index.html" dentro de la carpeta "templates" de forma automática
    return render_template("index.html", resultado=resultado)

if __name__ == "__main__":
    app.run(debug=True)
