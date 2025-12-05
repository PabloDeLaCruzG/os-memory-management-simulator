from flask import Flask, render_template, request, send_file
from main import Simulator
import os
import uuid
import shutil

app = Flask(__name__)

if not os.path.exists("static"):
    os.makedirs("static")


def cleanup_old_sessions(max_age_hours=1):
    """Limpia sesiones antiguas para liberar espacio."""
    import time

    static_dir = "static"
    if not os.path.exists(static_dir):
        return

    cutoff_time = time.time() - (max_age_hours * 3600)

    for item in os.listdir(static_dir):
        item_path = os.path.join(static_dir, item)
        if os.path.isdir(item_path) and len(item) >= 32:
            try:
                if os.path.getctime(item_path) < cutoff_time:
                    shutil.rmtree(item_path)
                    print(f"✓ Sesion antigua eliminada: {item}")
            except Exception as e:
                print(f"✗ Error limpiando {item}: {e}")


@app.route("/", methods=["GET", "POST"])
def index():
    # Limpiar sesiones antiguas al inicio
    cleanup_old_sessions(max_age_hours=1)

    if request.method == "POST":
        entry_file = request.files["entry_file"]
        algorithm = request.form["algorithm"]

        session_id = str(uuid.uuid4())
        temp_filename = f"temp_{session_id}.txt"
        entry_file.save(temp_filename)

        try:
            simulator = Simulator(temp_filename, session_id)
            simulator.run(algorithm)

            os.remove(temp_filename)

            return render_template(
                "results.html", history=simulator.state_history, session_id=session_id
            )
        except Exception as e:
            if os.path.exists(temp_filename):
                os.remove(temp_filename)
            return f"Ocurrio un error: {str(e)}"

    return render_template("index.html")


@app.route("/download/<session_id>")
def download_file(session_id):
    path = os.path.join("static", session_id, "particiones.txt")
    if os.path.exists(path):
        return send_file(path, as_attachment=True)
    return "Archivo no encontrado", 404


if __name__ == "__main__":
    app.run(debug=True)
