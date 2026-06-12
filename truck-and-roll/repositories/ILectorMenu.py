from abc import ABC, abstractmethod
from typing import List, Optional

# ISP poque es una interfaz especifica para operaciones de solo lectura del menu
# cualquier clase que quiera leer el menu debe implementar estos metodos
class ILectorMenu(ABC):
    @abstractmethod
    def listar_disponibles(self) -> List:
        pass            # devuelve solo los items disponibles (los que puede ver el cajero)

    @abstractmethod
    def buscar_por_id(self, item_id: int) -> Optional[object]:
        pass            # devuelve un item especifico o None si no existe