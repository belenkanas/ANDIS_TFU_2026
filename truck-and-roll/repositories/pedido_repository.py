from repositories.ILectorPedido import ILectorPedido
from repositories.IEscritorPedido import IEscritorPedido
from models.pedido import Pedido, ItemPedido, EstadoPedido
from typing import List, Optional

# Patrón Repository: abstrae el acceso a datos de pedidos
# implementa ambas interfaces porque es quien tiene acceso completo a los datos
class PedidoRepository(ILectorPedido, IEscritorPedido):
    def __init__(self):
        self._pedidos: dict = {
            1001: Pedido(
                numero=1001,
                estado=EstadoPedido.PENDIENTE,
                items=[
                    ItemPedido(menu_item_id=1, nombre="Hamburguesa clásica", cantidad=2, precio_unitario=320.0),
                    ItemPedido(menu_item_id=2, nombre="Papas fritas", cantidad=1, precio_unitario=150.0),
                    ItemPedido(menu_item_id=3, nombre="Gaseosa", cantidad=2, precio_unitario=90.0),
                ],
                total=970.0,
                metodo_pago="efectivo",
                resultado_pago={"ok": True, "mensaje": "Pago en efectivo registrado"},
            ),
            1002: Pedido(
                numero=1002,
                estado=EstadoPedido.EN_PREPARACION,
                items=[
                    ItemPedido(menu_item_id=4, nombre="Hamburguesa doble", cantidad=1, precio_unitario=450.0),
                    ItemPedido(menu_item_id=2, nombre="Papas fritas", cantidad=1, precio_unitario=150.0),
                    ItemPedido(menu_item_id=7, nombre="Agua mineral", cantidad=1, precio_unitario=70.0),
                ],
                total=670.0,
                metodo_pago="tarjeta",
                resultado_pago={"ok": True, "autorizacion": "TRX-1002"},
            ),
            1003: Pedido(
                numero=1003,
                estado=EstadoPedido.LISTO,
                items=[
                    ItemPedido(menu_item_id=1, nombre="Hamburguesa clásica", cantidad=1, precio_unitario=320.0),
                    ItemPedido(menu_item_id=3, nombre="Gaseosa", cantidad=1, precio_unitario=90.0),
                ],
                total=410.0,
                metodo_pago="mercadopago",
                resultado_pago={"ok": True, "payment_id": "MP-1003"},
            ),
            1004: Pedido(
                numero=1004,
                estado=EstadoPedido.ENTREGADO,
                items=[
                    ItemPedido(menu_item_id=4, nombre="Hamburguesa doble", cantidad=1, precio_unitario=450.0),
                    ItemPedido(menu_item_id=7, nombre="Agua mineral", cantidad=1, precio_unitario=70.0),
                ],
                total=520.0,
                metodo_pago="efectivo",
                resultado_pago={"ok": True, "mensaje": "Pedido ya entregado"},
            ),
        }
        self._next_numero = max(self._pedidos.keys(), default=1000) + 1

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