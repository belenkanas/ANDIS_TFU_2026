from repositories.ILectorPedido import ILectorPedido
from repositories.IEscritorPedido import IEscritorPedido
from models.pedido import Pedido
from typing import List, Optional

# Patrón Repository: abstrae el acceso a datos de pedidos
# implementa ambas interfaces porque es quien tiene acceso completo a los datos
class PedidoRepository(ILectorPedido, IEscritorPedido):
    def __init__(self):
        self._pedidos: dict = {}  # empieza vacio porque se va llenando con los pedidos del dia
        self._next_numero = 1001 

    def listar(self) -> List[Pedido]:
        # devuelve todos los pedidos (el cocinero va viendo la cola completa)
        return list(self._pedidos.values())

    def buscar_por_numero(self, numero: int) -> Optional[Pedido]:
        # devuelve el pedido o None si no existe ese numero
        return self._pedidos.get(numero)

    def guardar(self, pedido: Pedido) -> Pedido:
        # sobreescribe el pedido existente con los datos actualizados
        self._pedidos[pedido.numero] = pedido
        return pedido

    def crear(self, pedido: Pedido) -> Pedido:
        # asigna el numero de orden al pedido y lo guarda
        pedido = pedido.model_copy(update={"numero": self._next_numero})
        self._pedidos[self._next_numero] = pedido
        self._next_numero += 1
        return pedido