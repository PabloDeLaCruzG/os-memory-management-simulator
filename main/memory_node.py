"""
Nodo de memoria que representa una particion o hueco en la lista enlazada.
"""


class MemoryNode:
    """
    Representa un nodo en una lista doblemente enlazada,
    que simboliza una particion o un hueco en la memoria.
    """

    def __init__(
        self, start_address, size, state="libre", process_id=None, exit_time=None
    ):
        """
        Inicializa un nodo de memoria.

        Args:
            start_address (int): Direccion inicial de la particion
            size (int): Tamaño de la particion
            state (str): Estado del nodo ('libre' u 'ocupado')
            process_id (str): ID del proceso que ocupa el nodo (si esta ocupado)
            exit_time (int): Tiempo en el que el proceso saldra de memoria
        """
        self.start_address = start_address
        self.size = size
        self.state = state
        self.process_id = process_id
        self.exit_time = exit_time

        # Punteros para la lista doblemente enlazada
        self.next = None
        self.prev = None

    def __repr__(self):
        """
        Representacion en texto del nodo segun el formato requerido.
        Formato: [direccion proceso/hueco tamaño]
        """
        if self.state == "ocupado":
            return f"[{self.start_address} {self.process_id} {self.size}]"
        else:
            return f"[{self.start_address} hueco {self.size}]"

    def is_free(self):
        """Retorna True si el nodo esta libre."""
        return self.state == "libre"

    def is_occupied(self):
        """Retorna True si el nodo esta ocupado."""
        return self.state == "ocupado"
