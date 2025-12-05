"""
Funciones para generar visualizaciones graficas de la memoria.
"""

import matplotlib

# Configuracion para entornos web.
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def generate_memory_graph(node_list, actual_time, save_path):
    """
    Genera un grafico de barras horizontal que representa el estado de la memoria.

    Args:
        node_list (list): Lista de nodos MemoryNode
        actual_time (int): Tiempo actual de la simulacion
        save_path (str): Ruta donde guardar la imagen
    """
    fig, ax = plt.subplots(figsize=(10, 2))

    colors = {"ocupado": "#e74c3c", "libre": "#2ecc71"}

    labels = []
    positions = []
    sizes = []
    bar_colors = []

    for node in node_list:
        if node.state == "ocupado":
            label = f"{node.process_id}\n{node.size} KB"
        else:
            label = f"Hueco\n{node.size} KB"

        labels.append(label)
        positions.append(node.start_address)
        sizes.append(node.size)
        bar_colors.append(colors[node.state])

    # Dibujar barras horizontales
    ax.barh(
        y=[0] * len(positions),
        width=sizes,
        left=positions,
        height=1,
        color=bar_colors,
        align="edge",
        edgecolor="white",
        linewidth=1,
    )

    # Añadir etiquetas
    for i, (pos, size, label) in enumerate(zip(positions, sizes, labels)):
        ax.text(
            pos + size / 2,
            0.4,
            label,
            ha="center",
            va="center",
            color="white",
            fontweight="bold",
            fontsize=9,
        )

    ax.set_xlim(0, 2000)
    ax.set_ylim(0, 1)
    ax.set_yticks([])
    ax.set_xlabel("Direcciones de Memoria (KB)", fontweight="bold")
    ax.set_title(f"Estado de la Memoria en t={actual_time}", fontweight="bold", pad=10)
    ax.grid(axis="x", alpha=0.3, linestyle="--")

    plt.tight_layout()
    plt.savefig(save_path, dpi=100, bbox_inches="tight")
    plt.close(fig)
