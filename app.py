from flask import Flask, render_template, request, send_file
from gestormemoria import Simulator
import os
import uuid
import shutil

app = Flask(__name__)

# Asegurar que existe static
if not os.path.exists("static"):
    os.makedirs("static")


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        entry_file = request.files["entry_file"]
        algorithm = request.form["algorithm"]

        # Generar ID único para esta ejecución
        session_id = str(uuid.uuid4())

        # Guardar archivo de entrada temporalmente con nombre único
        temp_filename = f"temp_{session_id}.txt"
        entry_file.save(temp_filename)

        try:
            # Instanciar simulador con el session_id
            simulator = Simulator(temp_filename, session_id)
            simulator.run(algorithm)

            # Borrar archivo de entrada temporal
            os.remove(temp_filename)

            return render_template(
                "results.html", history=simulator.state_history, session_id=session_id
            )
        except Exception as e:
            if os.path.exists(temp_filename):
                os.remove(temp_filename)
            return f"Ocurrió un error: {str(e)}"

    return render_template("index.html")


@app.route("/download/<session_id>")
def download_file(session_id):
    # Permite descargar el particiones.txt generado
    path = os.path.join("static", session_id, "particiones.txt")
    if os.path.exists(path):
        return send_file(path, as_attachment=True)
    return "Archivo no encontrado"


if __name__ == "__main__":
    app.run(debug=True)
