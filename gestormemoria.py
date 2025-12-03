import sys
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import os
import math


class MemoryNode:
    """
    Representa un node en una lista de doble enlace,
    que simboliza una particion o un hueco en la memoria
    """

    def __init__(
        self, start_address, size, state="libre", process_id=None, exit_time=None
    ):
        self.start_address = start_address
        self.size = size
        self.state = state  # libre u ocupado
        self.process_id = process_id  # P1, P2 ... Pn
        self.exit_time = exit_time

        # Punteros para la lista
        self.next = None
        self.prev = None

    def __repr__(self):
        """
        Funcion que permite darle un formato mas facil de leer,
        variante de __str__
        """

        if self.state == "ocupado":
            return f"[{self.start_address} {self.process_id} {self.size}]"
        else:
            return f"[{self.start_address} hueco {self.size}]"


class MemoryManager:
    """
    Simula el gestor de memori.
    Maneja la lista de bloques de memoria
    """

    def __init__(self, memory_size=2000):
        self.memory_size = memory_size

        # Al inicio la memoria es solo un bloque libre con todo el tamaño
        self.head = MemoryNode(start_address=0, size=memory_size)

        # Puntero que guarda donde se hizo la ultima asignacion para el algoritmo de SIGUIENTE HUECO
        self.last_assigned_node = self.head

    def print_state(self, actual_time):
        """
        Recorre la lista de bloques e imprime el estado actual de la memoria
        """

        actual_node = self.head
        state_line = [f"{actual_time}"]

        while actual_node:
            state_line.append(str(actual_node))
            actual_node = actual_node.next
        print(" ".join(state_line))

    def put_first_gap(self, process_id, req_memory, actual_time, ejec_time):
        """
        Implementa el algoritmo de asignacion PRIMER HUECO.
        Recorre la memoria y asigna el proceso al primer hueco libre que vea que
        cabe.
        Devuelve true si se puedo asigna
        """

        actual_node = self.head

        while actual_node:
            # Busca un bloque libre y con tamaño suficiente
            if actual_node.state == "libre" and actual_node.size >= req_memory:
                # Hueco mas grande que la memoria requerida
                # Divide el bloque en dos, uno para el proceso y otro para el hueco que sobra
                if actual_node.size > req_memory:
                    # Nuevo bloque para el hueco que sobra
                    new_gap_address = actual_node.start_address + req_memory
                    new_gap_size = actual_node.size - req_memory

                    new_gap = MemoryNode(
                        start_address=new_gap_address, size=new_gap_size, state="libre"
                    )

                    # Reconectar punteros de la lista
                    og_next = actual_node.next

                    # bloque actual apunta al nuevo hueco
                    actual_node.next = new_gap
                    # nuevo hueco apunta al que era el siguiente del bloque actual
                    new_gap.next = og_next
                    # mnuevo hueco apunta atras al bloque actual
                    new_gap.prev = actual_node

                    # Si hay un bloque despues del original, se actualiza para que apunte al nuevo
                    if og_next:
                        og_next.prev = new_gap

                    # Actualiza el bloque actual para que represent al proceso
                    actual_node.size = req_memory

                # Actualizar bloque a ocupado
                actual_node.state = "ocupado"
                actual_node.process_id = process_id
                actual_node.exit_time = actual_time + ejec_time

                return True

            actual_node = actual_node.next

        print(
            f"No hay espacio suficiente para el proceso {process_id} con tamaño {req_memory}"
        )
        return False

    def release_memory(self, process_id):
        """
        Busca el proceso con el id dado, libera su bloque de memoria y fusiona el nuevo hueco
        con bloques adyacentes si tabien estan libres
        """

        node_to_release = self.head

        # Busca el bloque que ocupa el proceso
        while node_to_release and node_to_release.process_id != process_id:
            node_to_release = node_to_release.next

        # Si node_to_realease es None, siginifica que no se ha encontrado el proceso -> sale de la funcion
        if not node_to_release:
            print(
                f"Proceso {process_id} no encontrado en memoria. No se puede liberar."
            )
            return

        # Poner bloque como libre
        node_to_release.state = "libre"
        node_to_release.process_id = None
        node_to_release.exit_time = None

        # Logica de fusion (Coalescing)
        # Fusion con bloque next
        next_node = node_to_release.next
        if next_node and next_node.state == "libre":
            node_to_release.size += next_node.size
            node_to_release.next = (
                next_node.next
            )  # Salta el puntero siguiente del bloque actual para eliminar el bloque fusionado

            if next_node.next:
                next_node.next.prev = node_to_release

        # Fusion con bloque anterior
        prev_node = node_to_release.prev
        if prev_node and prev_node.state == "libre":
            prev_node.size += node_to_release.size
            prev_node.next = node_to_release.next

            if node_to_release.next:
                node_to_release.next.prev = prev_node

    def put_next_gap(self, process_id, req_memory, actual_time, ejec_time):
        """
        Implementa el algoritmo de asignacion SIGUIENTE HUECO.
        Busca desde el ultimo nodo donde se asigno la memoria
        """

        # si es none, se empieza por la cabeza
        first_node = self.last_assigned_node or self.head

        actual_node = first_node

        # Doble busqueda, del ultimo hasta el final. Si no se encuentra, del principio hasta el ultimo
        for i in range(2):
            while actual_node:
                if actual_node.state == "libre" and actual_node.size >= req_memory:
                    # Hueco encontrado
                    self.last_assigned_node = actual_node

                    if actual_node.size > req_memory:
                        new_gap_address = actual_node.start_address + req_memory
                        new_gap_size = actual_node.size - req_memory
                        new_gap = MemoryNode(
                            start_address=new_gap_address, size=new_gap_size
                        )

                        og_next = actual_node.next
                        actual_node.next = new_gap
                        new_gap.next = og_next
                        new_gap.prev = actual_node

                        if og_next:
                            og_next.prev = new_gap

                        actual_node.size = req_memory

                    actual_node.state = "ocupado"
                    actual_node.process_id = process_id
                    actual_node.exit_time = actual_time + ejec_time

                    return True

                actual_node = actual_node.next

            # Si llega aqui, prepara la siguiente pasada empezando del principio
            if i == 0:
                actual_node = self.head

        print(
            f"No hay espacio suficiente para el proceso {process_id} con tamaño {req_memory}"
        )
        return False


def generate_memory_graph(node_list, actual_time, save_path):
    """
    Genera un grafico de barras que representa el estado de la memoria y lo guarda en imagen
    """

    fig, ax = plt.subplots(figsize=(10, 2))

    colors = {"ocupado": "red", "libre": "green"}

    labels = []
    positions = []
    sizes = []
    bar_colors = []

    for node in node_list:

        if node.state == "ocupado":
            label = f"Proceso {node.process_id}\n{node.size} KB"
        else:
            label = f"Hueco\n{node.size} KB"

        labels.append(label)
        positions.append(node.start_address)
        sizes.append(node.size)
        bar_colors.append(colors[node.state])

    ax.barh(
        y=[0] * len(positions),
        width=sizes,
        left=positions,
        height=1,
        color=bar_colors,
        align="edge",
    )

    for i, (pos, size) in enumerate(zip(positions, sizes)):
        ax.text(
            pos + size / 2,
            0.4,
            labels[i],
            ha="center",
            va="center",
            color="white",
            fontweight="bold",
        )

    ax.set_xlim(0, 2000)  # Límite de la memoria
    ax.set_ylim(0, 1)
    ax.set_yticks([])  # Oculta el eje Y
    ax.set_xlabel("Direcciones de Memoria")
    ax.set_title(f"Estado de la Memoria en t={actual_time}")

    plt.tight_layout()
    plt.savefig(save_path)
    plt.close(fig)


class Process:
    """
    Almacena la informacion de un proceso leido desde el fichero de entrada
    """

    def __init__(self, id, arrival_moment, required_memory, execution_time):
        self.id = id
        self.arrival_moment = int(arrival_moment)

        # redondea hacia arriba
        mem_req = int(required_memory)
        if mem_req % 100 != 0:
            self.required_memory = ((mem_req // 100) + 1) * 100
        else:
            self.required_memory = mem_req

        self.execution_time = int(execution_time)
        self.original_memory = int(required_memory)

    def __repr__(self):
        return f"Proceso {self.id}, llega en {self.arrival_moment}, memoria requerida {self.original_memory} --> {self.required_memory}, tiempo de ejecucion {self.execution_time}"


class Simulator:
    def __init__(self, entry_file, session_id):

        self.pending_processes = self._load_processes(entry_file)
        self.memory_manager = MemoryManager()
        self.actual_time = 0
        self.state_history = []
        self.session_id = session_id

        # Crea carpeta para la sesion
        self.session_dir = os.path.join("static", self.session_id)
        if not os.path.exists(self.session_dir):
            os.makedirs(self.session_dir)

        # Archivo de salida
        self.output_file = os.path.join(self.session_dir, "particiones.txt")
        open(self.output_file, "w").close()  # Limpia archivo de salida

    def _load_processes(self, entry_file):
        """
        Metodo privado para leer el archivo y crear la lista de procesos
        """
        processes = []
        try:
            with open(entry_file, "r") as f:
                for line in f:
                    parts = line.strip().split()
                    if len(parts) == 4:
                        process = Process(*parts)
                        processes.append(process)
        except FileNotFoundError:
            print(f"Error: El archivo '{entry_file}' no fue encontrado.")
            sys.exit(1)  # O manejar el error de otra forma en un entorno web
        return processes

    def _iter_nodes(self):
        """
        Un generador para iterar facilmente sobre los bloques de memoria
        """
        node = self.memory_manager.head
        while node:
            yield node
            node = node.next

    def _state_add(self, event_description="", error=False):
        """
        Registra el estado actual (texto y grafico) y lo añade al historial
        """
        nodes = list(self._iter_nodes())
        partitions_str = [str(node) for node in nodes]
        txt_state = f"{self.actual_time} " + " ".join(partitions_str)

        # Si no hay error, genera el grafico
        web_graph_path = None
        if not error:
            # Guarda imagen en la carpeta de la sesion
            graph_filename = f"memory_t{self.actual_time}_{len(self.state_history)}.png"
            graph_path_rel = os.path.join(self.session_dir, graph_filename)
            generate_memory_graph(nodes, self.actual_time, graph_path_rel)
            # Guarda en el historial de la web
            web_graph_path = f"{self.session_id}/{graph_filename}"

        self.state_history.append(
            {
                "time": self.actual_time,
                "text": txt_state,
                "graph": web_graph_path,
                "event": event_description,
                "is_error": error,
            }
        )

        # Escribe en particiones.txt el estado
        with open(self.output_file, "a") as f:
            f.write(f"{txt_state}\n")

    def run(self, algorithm):
        """
        Bucle principal de la simulacion
        """
        # Registra y guarda el estado inicial (t=0)
        self._state_add("Inicio de la simulacion")

        # El bucle se ejecuta mientras haya procesos por llegar o procesos en memoria.
        while self.pending_processes or any(
            b.state == "ocupado" for b in self._iter_nodes()
        ):

            # Avanzamos el tiempo al siguiente evento para ser más eficientes
            next_arrival_time = (
                self.pending_processes[0].arrival_moment
                if self.pending_processes
                else float("inf")
            )

            exit_times = [
                b.exit_time
                for b in self._iter_nodes()
                if b.state == "ocupado" and b.exit_time is not None
            ]
            next_exit_time = min(exit_times) if exit_times else float("inf")

            next_event_time = min(next_arrival_time, next_exit_time)

            if next_event_time == float("inf"):
                break  # No hay mas eventos, sale del bucle

            self.actual_time = next_event_time

            # 1. Salidas
            released = []
            for node in self._iter_nodes():
                if node.state == "ocupado" and node.exit_time == self.actual_time:
                    released.append(node.process_id)

            if released:
                for pid in released:
                    self.memory_manager.release_memory(pid)
                # Registramos la salida
                self._state_add(f"Salida: {', '.join(released)}")

            # 2. Llegadas
            if (
                self.pending_processes
                and self.pending_processes[0].arrival_moment == self.actual_time
            ):
                proc = self.pending_processes.pop(0)

                if algorithm == "first_fit":
                    assigned = self.memory_manager.put_first_gap(
                        proc.id,
                        proc.required_memory,
                        self.actual_time,
                        proc.execution_time,
                    )
                else:
                    assigned = self.memory_manager.put_next_gap(
                        proc.id,
                        proc.required_memory,
                        self.actual_time,
                        proc.execution_time,
                    )

                if assigned:
                    event_desc = f"Llegada {proc.id} (Req: {proc.original_memory} -> Asig: {proc.required_memory})"
                    self._state_add(event_desc)
                else:
                    # Error: proceso no cabe - agregar solo mensaje, NO cambiar estado
                    error_msg = f"Llegada {proc.id} - ¡FALLO! No hay memoria (Req: {proc.original_memory} → {proc.required_memory})"
                    self.state_history.append({
                        "time": self.actual_time,
                        "text": "",
                        "graph": None,
                        "event": error_msg,
                        "is_error": True,
                    })
