# 💻 Simulador de Gestión de Memoria con Particiones Variables

Este proyecto es un simulador desarrollado para la asignatura de Sistemas Operativos. Implementa y visualiza algoritmos de gestión de memoria dinámica (particiones variables) como **Primer Hueco (First-Fit)** y **Siguiente Hueco (Next-Fit)** a través de una interfaz web interactiva.

---

## ✨ Características Principales

*   **Simulación Basada en Eventos:** El simulador procesa una lista de procesos desde un archivo de entrada, gestionando sus llegadas y salidas en el tiempo.
*   **Algoritmos de Asignación:**
    *   Primer Hueco (First-Fit).
    *   Siguiente Hueco (Next-Fit).
*   **Interfaz Web con Flask:** Permite al usuario subir su propio archivo de procesos, elegir el algoritmo y ver los resultados en el navegador.
*   **Visualización Gráfica con Matplotlib:** Genera un gráfico de barras del estado de la memoria en cada instante de tiempo, facilitando la comprensión del comportamiento de los algoritmos.
*   **Gestión de Memoria Dinámica:** Simula la asignación, la división de huecos, la liberación y la fusión (coalescing) de huecos adyacentes.
*   **Registro de Salida:** Genera un archivo `particiones.txt` con el historial del estado de la memoria, siguiendo el formato requerido por la práctica.

---

## 🛠️ Tecnologías Utilizadas

*   **Backend:** Python 3
*   **Framework Web:** Flask
*   **Visualización:** Matplotlib
*   **Frontend:** HTML5 / CSS3

---

## 🚀 Cómo Ponerlo en Marcha

Sigue estos pasos para ejecutar el simulador en tu máquina local.

### 1. Prerrequisitos

*   Tener Python 3 instalado.

### 2. Instalación

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

### 3. Ejecución

1.  **Inicia la aplicación Flask:**
    ```bash
    python app.py
    ```

2.  **Abre tu navegador** y ve a la siguiente dirección:
    [http://127.0.0.1:5000](http://127.0.0.1:5000)

3.  **Usa la interfaz:**
    *   Sube un archivo `entrada.txt`.
    *   Selecciona el algoritmo de asignación que deseas probar.
    *   Haz clic en "Ejecutar Simulación" y observa los resultados.

---

## 📄 Formato del Archivo de Entrada

El archivo `entrada.txt` debe contener un proceso por línea, con los campos separados por espacios, siguiendo este formato:

`<ID_Proceso> <Instante_Llegada> <Memoria_Requerida> <Tiempo_Ejecución>`

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
├── app.py                  # Lógica del servidor Flask
├── gestormemoria.py        # Clases principales del simulador (MemoryManager, Simulator)
├── requirements.txt        # Dependencias de Python
├── entrada.txt             # Archivo de ejemplo
├── templates/
│   ├── index.html          # Página de inicio con el formulario
│   └── results.html        # Página que muestra los resultados
└── static/                 # Carpeta para guardar los gráficos generados
```

---

## 👨‍💻 Autor

*   **Pablo De La Cruz Gómez** - [PabloDeLaCruzG](https://github.com/PabloDeLaCruzG)

Este proyecto fue desarrollado como parte de la Práctica 3 de la asignatura de Sistemas Operativos.