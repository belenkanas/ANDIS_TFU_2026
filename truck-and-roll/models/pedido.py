from pydantic import BaseModel
from typing import List, Optional
from enum import Enum

# se definen los unicos estados posibles de un pedido
class EstadoPedido(str, Enum):
    PENDIENTE = "PENDIENTE"
    EN_PREPARACION = "EN_PREPARACION"
    LISTO = "LISTO"
    ENTREGADO = "ENTREGADO"

# Patrón State: define que transiciones son validas
# un pedido solo puede avanzar en orden, nunca saltarse pasos ni retroceder
TRANSICIONES_VALIDAS = {
    EstadoPedido.PENDIENTE: [EstadoPedido.EN_PREPARACION],
    EstadoPedido.EN_PREPARACION: [EstadoPedido.LISTO],
    EstadoPedido.LISTO: [EstadoPedido.ENTREGADO],
    EstadoPedido.ENTREGADO: [],
}

# representa un item dentro de un pedido con su cantidad y precio al momento de la compra
class ItemPedido(BaseModel):
    menu_item_id: int
    nombre: str
    cantidad: int
    precio_unitario: float

# representa un pedido completo en el sistema
class Pedido(BaseModel):
    numero: int                                     # se asigna automaticamente
    estado: EstadoPedido = EstadoPedido.PENDIENTE   # siempre arranca como pendiente
    items: List[ItemPedido]
    total: float
    metodo_pago: str                                 # efectivo, tarjeta o mercadopago
    resultado_pago: Optional[dict] = None            # respuesta de la estrategia de pago

# datos que recibe la api al crear un nuevo pedido - PUC001
class PedidoCreate(BaseModel):
    items: List[dict]  # [{"menu_item_id": 1, "cantidad": 2}]
    metodo_pago: str   # efectivo, tarjeta, mercadopago

# dato que recibe la api al cambiar el estado de un pedido - PUC002
class CambioEstado(BaseModel):
    nuevo_estado: EstadoPedido      # debe ser un valor valido de EstadoPedido
