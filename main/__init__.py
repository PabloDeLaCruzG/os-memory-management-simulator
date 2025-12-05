"""
Modulo principal de gestion de memoria.
Contiene las clases principales del simulador.
"""

from .memory_node import MemoryNode
from .memory_manager import MemoryManager
from .process import Process
from .simulator import Simulator

__all__ = ["MemoryNode", "MemoryManager", "Process", "Simulator"]
