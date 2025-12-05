"""
Clase que representa un proceso del sistema.
"""


class Process:
    """
    Almacena la informacion de un proceso leido desde el fichero de entrada.
    """

    ALLOCATION_UNIT = 100  # Unidad minima de asignacion

    def __init__(self, id, arrival_moment, required_memory, execution_time):
        """
        Inicializa un proceso.

        Args:
            id (str): Identificador del proceso
            arrival_moment (str|int): Momento de llegada
            required_memory (str|int): Memoria requerida
            execution_time (str|int): Tiempo de ejecucion
        """
        self.id = id
        self.arrival_moment = int(arrival_moment)
        self.original_memory = int(required_memory)
        self.execution_time = int(execution_time)

        # Redondear hacia arriba a multiplos de ALLOCATION_UNIT
        self.required_memory = self._round_to_allocation_unit(self.original_memory)

    def _round_to_allocation_unit(self, size):
        """
        Redondea el tamaño hacia arriba al multiplo de la unidad de asignacion.

        Args:
            size (int): Tamaño a redondear

        Returns:
            int: Tamaño redondeado
        """
        if size % self.ALLOCATION_UNIT != 0:
            return ((size // self.ALLOCATION_UNIT) + 1) * self.ALLOCATION_UNIT
        return size

    @property
    def exit_time(self):
        """Calcula el momento en que el proceso saldra de memoria."""
        return self.arrival_moment + self.execution_time

    def __repr__(self):
        return (
            f"Proceso {self.id}, llega en {self.arrival_moment}, "
            f"memoria requerida {self.original_memory} → {self.required_memory}, "
            f"tiempo de ejecucion {self.execution_time}"
        )
