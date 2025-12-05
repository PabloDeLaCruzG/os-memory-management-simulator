# 💻 Simulador de Gestion de Memoria con Particiones Variables

Este proyecto es un simulador desarrollado para la asignatura de Sistemas Operativos. Implementa y visualiza algoritmos de gestion de memoria dinamica (particiones variables) como **Primer Hueco (First-Fit)** y **Siguiente Hueco (Next-Fit)** a través de una interfaz web interactiva.

---

## ✨ Caracteristicas Principales

*   **Simulacion Basada en Eventos:** El simulador procesa una lista de procesos desde un archivo de entrada, gestionando sus llegadas y salidas en el tiempo.
*   **Algoritmos de Asignacion:**
    *   Primer Hueco (First-Fit).
    *   Siguiente Hueco (Next-Fit).
*   **Interfaz Web con Flask:** Permite al usuario subir su propio archivo de procesos, elegir el algoritmo y ver los resultados en el navegador.
*   **Visualizacion Grafica con Matplotlib:** Genera un grafico de barras del estado de la memoria en cada instante de tiempo, facilitando la comprension del comportamiento de los algoritmos.
*   **Gestion de Memoria Dinamica:** Simula la asignacion, la division de huecos, la liberacion y la fusion (coalescing) de huecos adyacentes.
*   **Registro de Salida:** Genera un archivo `particiones.txt` con el historial del estado de la memoria, siguiendo el formato requerido por la practica.

---

## 🛠️ Tecnologias Utilizadas

*   **Backend:** Python 3
*   **Framework Web:** Flask
*   **Visualizacion:** Matplotlib
*   **Frontend:** HTML5 / CSS3

---

## 🚀 Como Ponerlo en Marcha

Sigue estos pasos para ejecutar el simulador en tu maquina local.

### 1. Prerrequisitos

*   Tener Python 3 instalado.

### 2. Instalacion

1.  **Clona el repositorio:**
    ```bash
    git clone https://github.com/tu-usuario/os-memory-management-simulator.git
    cd os-memory-management-simulator
    ```

2.  **(Recomendado) Crea y activa un entorno virtual:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # En Windows: venv\Scripts\activate
    ```

3.  **Instala las dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

### 3. Ejecucion

1.  **Inicia la aplicacion Flask:**
    ```bash
    python app.py
    ```

2.  **Abre tu navegador** y ve a la siguiente direccion:
    [http://127.0.0.1:5000](http://127.0.0.1:5000)

3.  **Usa la interfaz:**
    *   Sube un archivo `entrada.txt`.
    *   Selecciona el algoritmo de asignacion que deseas probar.
    *   Haz clic en "Ejecutar Simulacion" y observa los resultados.

---

## 📄 Formato del Archivo de Entrada

El archivo `entrada.txt` debe contener un proceso por linea, con los campos separados por espacios, siguiendo este formato:

`<ID_Proceso> <Instante_Llegada> <Memoria_Requerida> <Tiempo_Ejecucion>`

**Ejemplo:**
```
P1 1 500 6
P2 2 700 3
P3 3 1000 5
```

---

## 📂 Estructura del Proyecto

```
.
├── app.py                  # Logica del servidor Flask
├── gestormemoria.py        # Clases principales del simulador (MemoryManager, Simulator)
├── requirements.txt        # Dependencias de Python
├── entrada.txt             # Archivo de ejemplo
├── templates/
│   ├── index.html          # Pagina de inicio con el formulario
│   └── results.html        # Pagina que muestra los resultados
└── static/                 # Carpeta para guardar los graficos generados
```

---

## 👨‍💻 Autor

*   **Pablo De La Cruz Gomez** - [PabloDeLaCruzG](https://github.com/PabloDeLaCruzG)

Este proyecto fue desarrollado como parte de la Practica 3 de la asignatura de Sistemas Operativos.