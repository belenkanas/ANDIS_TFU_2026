from abc import ABC, abstractmethod

# ISP porque es una interfaz especifica para operaciones de escritura de pedidos
# solo quien necesita crear o modificar pedidos depende de esta interfaz
class IEscritorPedido(ABC):
    @abstractmethod
    def guardar(self, pedido) -> object:
        pass                # actualiza un pedido existente

    @abstractmethod
    def crear(self, pedido) -> object:
        pass                # registra un pedido nuevo en el sistema - PUC001