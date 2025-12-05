"""
Simulador principal que coordina la gestion de memoria.
"""

import sys
import os
from .memory_manager import MemoryManager
from .process import Process
from utils.graphics import generate_memory_graph


class Simulator:
    """
    Coordina la simulacion de gestion de memoria.
    """

    def __init__(self, entry_file, session_id):
        """
        Inicializa el simulador.

        Args:
            entry_file (str): Ruta al archivo de entrada
            session_id (str): ID unico de la sesion
        """
        self.pending_processes = self._load_processes(entry_file)
        self.memory_manager = MemoryManager()
        self.actual_time = 0
        self.state_history = []
        self.session_id = session_id

        # Crear carpeta para la sesion
        self.session_dir = os.path.join("static", self.session_id)
        os.makedirs(self.session_dir, exist_ok=True)

        # Archivo de salida
        self.output_file = os.path.join(self.session_dir, "particiones.txt")
        open(self.output_file, "w").close()

    def _load_processes(self, entry_file):
        """
        Lee el archivo de entrada y crea la lista de procesos.

        Args:
            entry_file (str): Ruta al archivo

        Returns:
            list: Lista de objetos Process
        """
        processes = []
        try:
            with open(entry_file, "r") as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    if not line:
                        continue

                    parts = line.split()
                    if len(parts) != 4:
                        print(f"⚠️ Linea {line_num} ignorada (formato incorrecto)")
                        continue

                    try:
                        process = Process(*parts)
                        processes.append(process)
                    except ValueError as e:
                        print(f"❌ Error en linea {line_num}: {e}")

        except FileNotFoundError:
            print(f"Error: El archivo '{entry_file}' no fue encontrado.")
            sys.exit(1)

        return processes

    def _iter_nodes(self):
        """Generador para iterar sobre los nodos de memoria."""
        node = self.memory_manager.head
        while node:
            yield node
            node = node.next

    def _state_add(self, event_description="", error=False):
        """
        Registra el estado actual y lo guarda.

        Args:
            event_description (str): Descripcion del evento
            error (bool): Indica si es un error
        """
        nodes = list(self._iter_nodes())
        partitions_str = [str(node) for node in nodes]
        txt_state = f"{self.actual_time} " + " ".join(partitions_str)

        web_graph_path = None
        if not error:
            graph_filename = f"memory_t{self.actual_time}_{len(self.state_history)}.png"
            graph_path_rel = os.path.join(self.session_dir, graph_filename)
            generate_memory_graph(nodes, self.actual_time, graph_path_rel)
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

        with open(self.output_file, "a") as f:
            f.write(f"{txt_state}\n")

    def run(self, algorithm):
        """
        Ejecuta la simulacion con el algoritmo especificado.

        Args:
            algorithm (str): 'first_fit' o 'next_fit'
        """
        self._state_add("Inicio de la simulacion")

        while self.pending_processes or any(
            b.is_occupied() for b in self._iter_nodes()
        ):
            next_event_time = self._calculate_next_event()

            if next_event_time == float("inf"):
                break

            self.actual_time = next_event_time

            # Procesar salidas
            self._process_exits()

            # Procesar llegadas
            self._process_arrivals(algorithm)

    def _calculate_next_event(self):
        """Calcula el tiempo del proximo evento."""
        next_arrival = (
            self.pending_processes[0].arrival_moment
            if self.pending_processes
            else float("inf")
        )

        exit_times = [
            b.exit_time
            for b in self._iter_nodes()
            if b.is_occupied() and b.exit_time is not None
        ]
        next_exit = min(exit_times) if exit_times else float("inf")

        return min(next_arrival, next_exit)

    def _process_exits(self):
        """Procesa las salidas de procesos en el tiempo actual."""
        released = [
            node.process_id
            for node in self._iter_nodes()
            if node.is_occupied() and node.exit_time == self.actual_time
        ]

        if released:
            for pid in released:
                self.memory_manager.release_memory(pid)
            self._state_add(f"Salida: {', '.join(released)}")

    def _process_arrivals(self, algorithm):
        """
        Procesa las llegadas de procesos en el tiempo actual.

        Args:
            algorithm (str): Algoritmo de asignacion a usar
        """
        if not self.pending_processes:
            return

        if self.pending_processes[0].arrival_moment != self.actual_time:
            return

        proc = self.pending_processes.pop(0)

        # Seleccionar algoritmo
        if algorithm == "first_fit":
            assigned = self.memory_manager.put_first_gap(
                proc.id, proc.required_memory, self.actual_time, proc.execution_time
            )
        else:  # next_fit
            assigned = self.memory_manager.put_next_gap(
                proc.id, proc.required_memory, self.actual_time, proc.execution_time
            )

        if assigned:
            event = f"Llegada {proc.id} (Req: {proc.original_memory} → Asig: {proc.required_memory})"
            self._state_add(event)
        else:
            error_msg = f"Llegada {proc.id} - ¡FALLO! No hay memoria (Req: {proc.original_memory} → {proc.required_memory})"
            self.state_history.append(
                {
                    "time": self.actual_time,
                    "text": "",
                    "graph": None,
                    "event": error_msg,
                    "is_error": True,
                }
            )
