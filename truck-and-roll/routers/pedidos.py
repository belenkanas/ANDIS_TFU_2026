from fastapi import APIRouter
from services.pedido_service import PedidoService
from models.pedido import PedidoCreate, CambioEstado

# agrupa todos los endpoints de pedidos bajo /pedidos
router = APIRouter(prefix="/pedidos", tags=["Pedidos"])  # tags agrupa los endpoints en el /docs

# DIP - recibe el service como parametro en vez de instanciarlo aca
def get_router(service: PedidoService) -> APIRouter:

    # cajero registra un pedido nuevo con los items y metodo de pago
    # Pydantic valida automaticamente que los datos tengan el formato correcto
    @router.post("/", summary="Registrar nuevo pedido - PUC001")
    def registrar_pedido(data: PedidoCreate):
        return service.registrar_pedido(data)

    # cocinero o cajero consultan todos los pedidos activos
    @router.get("/", summary="Ver cola de pedidos - PUC002")
    def listar_pedidos():
        return service.listar_pedidos()

    # consulta un pedido especifico por su numero de orden
    @router.get("/{numero}", summary="Ver detalle de un pedido")
    def obtener_pedido(numero: int):
        return service.obtener_pedido(numero)

    # cocinero cambia el estado del pedido (PENDIENTE → EN PREPARACION → LISTO)
    # State valida que la transicion sea permitida
    @router.patch("/{numero}/estado", summary="Cambiar estado - PUC002")
    def cambiar_estado(numero: int, data: CambioEstado):
        return service.cambiar_estado(numero, data.nuevo_estado)

    # cajero confirma que entrego el pedido al cliente
    # State valida que el pedido este LISTO antes de permitir ENTREGADO
    @router.patch("/{numero}/entregar", summary="Marcar pedido entregado - PUC003")
    def entregar_pedido(numero: int):
        return service.entregar_pedido(numero)

    return router