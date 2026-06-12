from fastapi import APIRouter
from services.menu_service import MenuService
from models.menu_item import MenuItemCreate, MenuItemUpdate

# agrupa todos los endpoints de menu bajo /menu
router = APIRouter(prefix="/menu", tags=["Menú"])  # tags agrupa los endpoints en el /docs

# recibe el service como parametro en vez de instanciarlo aca - DIP
def get_router(service: MenuService) -> APIRouter:

    # cajero consulta los items disponibles antes de tomar un pedido
    @router.get("/", summary="Ver menú disponible")
    def obtener_menu():
        return service.obtener_menu_disponible()

    # dueño agrega un item nuevo, Pydantic valida automaticamente los datos
    @router.post("/", summary="Agregar ítem al menú")
    def agregar_item(data: MenuItemCreate):
        return service.agregar_item(data)

    # dueño modifica o deshabilita un item existente
    # PATCH en vez de PUT porque no es obligatorio mandar todos los campos
    @router.patch("/{item_id}", summary="Modificar ítem del menú (dueño)")
    def actualizar_item(item_id: int, data: MenuItemUpdate):
        return service.actualizar_item(item_id, data)

    return router