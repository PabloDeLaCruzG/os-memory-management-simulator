"""
Gestor de memoria que implementa los algoritmos de asignacion.
"""

from .memory_node import MemoryNode


class MemoryManager:
    """
    Simula el gestor de memoria.
    Maneja la lista de bloques de memoria y los algoritmos de asignacion.
    """

    def __init__(self, memory_size=2000):
        """
        Inicializa el gestor de memoria.

        Args:
            memory_size (int): Tamaño total de la memoria
        """
        self.memory_size = memory_size

        # Al inicio la memoria es solo un bloque libre con todo el tamaño
        self.head = MemoryNode(start_address=0, size=memory_size)

        # Puntero para el algoritmo de SIGUIENTE HUECO
        self.last_assigned_node = self.head

    def print_state(self, actual_time):
        """
        Imprime el estado actual de la memoria en consola.

        Args:
            actual_time (int): Tiempo actual de la simulacion
        """
        actual_node = self.head
        state_line = [f"{actual_time}"]

        while actual_node:
            state_line.append(str(actual_node))
            actual_node = actual_node.next

        print(" ".join(state_line))

    def put_first_gap(self, process_id, req_memory, actual_time, ejec_time):
        """
        Implementa el algoritmo PRIMER HUECO (First-Fit).
        Recorre la memoria desde el inicio y asigna el proceso al primer
        hueco libre que sea suficientemente grande.

        Args:
            process_id (str): ID del proceso a asignar
            req_memory (int): Memoria requerida por el proceso
            actual_time (int): Tiempo actual
            ejec_time (int): Tiempo de ejecucion del proceso

        Returns:
            bool: True si se pudo asignar, False en caso contrario
        """
        actual_node = self.head

        while actual_node:
            if actual_node.is_free() and actual_node.size >= req_memory:
                # Dividir el bloque si es necesario
                if actual_node.size > req_memory:
                    self._split_node(actual_node, req_memory)

                # Asignar el proceso al bloque
                actual_node.state = "ocupado"
                actual_node.process_id = process_id
                actual_node.exit_time = actual_time + ejec_time

                return True

            actual_node = actual_node.next

        print(
            f"No hay espacio suficiente para el proceso {process_id} con tamaño {req_memory}"
        )
        return False

    def put_next_gap(self, process_id, req_memory, actual_time, ejec_time):
        """
        Implementa el algoritmo SIGUIENTE HUECO (Next-Fit).
        Busca desde el ultimo nodo donde se asigno memoria, realizando
        una busqueda circular si es necesario.

        Args:
            process_id (str): ID del proceso a asignar
            req_memory (int): Memoria requerida
            actual_time (int): Tiempo actual
            ejec_time (int): Tiempo de ejecucion

        Returns:
            bool: True si se pudo asignar, False en caso contrario
        """
        first_node = self.last_assigned_node or self.head
        actual_node = first_node

        # Busqueda circular: del ultimo hasta el final, luego del inicio hasta el ultimo
        for _ in range(2):
            while actual_node:
                if actual_node.is_free() and actual_node.size >= req_memory:
                    self.last_assigned_node = actual_node

                    if actual_node.size > req_memory:
                        self._split_node(actual_node, req_memory)

                    actual_node.state = "ocupado"
                    actual_node.process_id = process_id
                    actual_node.exit_time = actual_time + ejec_time

                    return True

                actual_node = actual_node.next

            # Segunda pasada: volver al inicio
            actual_node = self.head

        print(
            f"No hay espacio suficiente para el proceso {process_id} con tamaño {req_memory}"
        )
        return False

    def release_memory(self, process_id):
        """
        Libera la memoria ocupada por un proceso y fusiona huecos adyacentes.

        Args:
            process_id (str): ID del proceso a liberar
        """
        node_to_release = self._find_process_node(process_id)

        if not node_to_release:
            print(f"Proceso {process_id} no encontrado en memoria.")
            return

        # Liberar el nodo
        node_to_release.state = "libre"
        node_to_release.process_id = None
        node_to_release.exit_time = None

        # Fusionar con nodos adyacentes libres
        self._coalesce(node_to_release)

    def _split_node(self, node, size):
        """
        Divide un nodo en dos: uno del tamaño especificado y otro con el resto.

        Args:
            node (MemoryNode): Nodo a dividir
            size (int): Tamaño del primer fragmento
        """
        new_gap_address = node.start_address + size
        new_gap_size = node.size - size

        new_gap = MemoryNode(
            start_address=new_gap_address, size=new_gap_size, state="libre"
        )

        # Reconectar punteros
        og_next = node.next
        node.next = new_gap
        new_gap.next = og_next
        new_gap.prev = node

        if og_next:
            og_next.prev = new_gap

        node.size = size

    def _find_process_node(self, process_id):
        """
        Busca el nodo que contiene un proceso especifico.

        Args:
            process_id (str): ID del proceso a buscar

        Returns:
            MemoryNode: Nodo encontrado o None
        """
        node = self.head
        while node:
            if node.process_id == process_id:
                return node
            node = node.next
        return None

    def _coalesce(self, node):
        """
        Fusiona un nodo libre con sus vecinos libres adyacentes.

        Args:
            node (MemoryNode): Nodo a fusionar con sus vecinos
        """
        # Fusion con el nodo siguiente
        next_node = node.next
        if next_node and next_node.is_free():
            node.size += next_node.size
            node.next = next_node.next
            if next_node.next:
                next_node.next.prev = node

        # Fusion con el nodo anterior
        prev_node = node.prev
        if prev_node and prev_node.is_free():
            prev_node.size += node.size
            prev_node.next = node.next
            if node.next:
                node.next.prev = prev_node
