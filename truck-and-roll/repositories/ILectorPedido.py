from abc import ABC, abstractmethod
from typing import List, Optional

# ISP porque es una interfaz especifica para operaciones de solo lectura de pedidos
# cualquier clase que necesite consultar pedidos depende de esta interfaz
class ILectorPedido(ABC):
    @abstractmethod
    def listar(self) -> List:
        pass            # devuelve todos los pedidos 

    @abstractmethod
    def buscar_por_numero(self, numero: int) -> Optional[object]:
        pass            # devuelve un pedido especifico o None si no existe