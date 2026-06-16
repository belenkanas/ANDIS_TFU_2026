from fastapi import FastAPI
from repositories.pedido_repository import PedidoRepository 
from repositories.menu_repository import MenuRepository
from services.pedido_service import PedidoService  
from services.menu_service import MenuService 
from patterns.observer import GestorObservadores, NotificacionClienteObserver, RegistroAuditoriaObserver
from routers import pedidos, menu

app = FastAPI(
    title="Truck & Roll",
    description="""Backend REST para el sistema de gestión de food trucks **Truck & Roll**

## Casos de Uso de Producto implementados
- **PUC001** – Registrar pedido
- **PUC002** – Actualizar estado del pedido 
- **PUC003** – Marcar pedido como entregado
- **PUC004** – Notificar al cliente cuando el pedido está listo
    """
)

menu_repo = MenuRepository()
pedido_repo = PedidoRepository()

gestor = GestorObservadores()
gestor.suscribir(NotificacionClienteObserver())  
gestor.suscribir(RegistroAuditoriaObserver()) 

menu_service = MenuService(menu_repo)
pedido_service = PedidoService(pedido_repo, menu_repo, gestor)

app.include_router(menu.get_router(menu_service))
app.include_router(pedidos.get_router(pedido_service))

@app.get("/", tags=["Root"])
def root():
    return {
        "mensaje": "Truck & Roll corriendo",
        "docs": "Visitá /docs para probar los endpoints",
    }