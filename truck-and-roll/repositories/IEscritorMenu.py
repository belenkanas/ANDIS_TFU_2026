from abc import ABC, abstractmethod

# ISP porque es una interfaz especifica para operaciones de escritura del menu
# solo el dueño, a traves de MenuAdminService, depende de esta interfaz
class IEscritorMenu(ABC):
    @abstractmethod
    def guardar(self, item) -> object:
        pass            # actualiza un item existente

    @abstractmethod
    def crear(self, nombre: str, descripcion: str, precio: float) -> object:
        pass            # agrega un item nuevo al menu