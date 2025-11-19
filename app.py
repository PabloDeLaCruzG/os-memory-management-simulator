from flask import Flask, render_template, request, redirect, url_for
from gestormemoria import Simulator
import os

app = Flask(__name__)

if not os.path.exists('static'): # para guardar las imagenes
    os.makedirs('static')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Recoge datos del formulario
        entry_file = request.files['entry_file']
        algorithm = request.form['algorithm']

        # Guardar en archuvo temporal
        file_path = 'temp_entry.txt'
        entry_file.save(file_path)

        # Crea y ejecuta la simulacion
        simulator = Simulator(file_path)
        simulator.run(algorithm)

        # Pasa los resultados al HTML
        return render_template('results.html', history=simulator.state_history)

    # Si la peticion es un GET muestra la pantalla de inicio
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)