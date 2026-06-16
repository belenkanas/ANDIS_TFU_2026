from repositories.ILectorMenu import ILectorMenu
from models.menu_item import MenuItem, MenuItemCreate, MenuItemUpdate
from typing import List
from fastapi import HTTPException

# ISP - MenuConsultaService solo depende de ILectorMenu
# el cajero nunca tiene acceso a metodos de escritura que no le corresponden
class MenuConsultaService:
    """Cajero viendo el menú"""
    def __init__(self, repo: ILectorMenu):
        self._repo = repo

    def obtener_menu_disponible(self) -> List[MenuItem]:
        # delega al repository, que sabe como filtrar los disponibles
        return self._repo.listar_disponibles()


# ISP - MenuAdminService accede a lectura y escritura
# el dueño puede tanto consultar como modificar el menu
class MenuAdminService:
    """Dueño gestionando el menú"""
    def __init__(self, repo: ILectorMenu):  
        self._repo = repo

    def agregar_item(self, data: MenuItemCreate) -> MenuItem:
        # delega la creacion al repository con los datos del request
        return self._repo.crear(data.nombre, data.descripcion, data.precio)

    def actualizar_item(self, item_id: int, data: MenuItemUpdate) -> MenuItem:
        item = self._repo.buscar_por_id(item_id)
        if not item:
            raise HTTPException(status_code=404, detail="Ítem no encontrado")
        actualizado = item.model_copy(update=data.model_dump(exclude_none=True))  # model_copy actualiza solo los campos que mando el dueño, ignora los None
        return self._repo.guardar(actualizado)

    def eliminar_item(self, item_id: int) -> dict:
        if not self._repo.buscar_por_id(item_id):
            raise HTTPException(status_code=404, detail="Ítem no encontrado")

        self._repo.eliminar(item_id)
        return {"ok": True, "mensaje": "Ítem eliminado"}


# el router habla con MenuService y no necesita saber que hay dos services adentro
class MenuService:
    def __init__(self, repo):
        self._consulta = MenuConsultaService(repo)  # para operaciones del cajero
        self._admin = MenuAdminService(repo)  # para operaciones del dueño

    def obtener_menu_disponible(self):
        return self._consulta.obtener_menu_disponible()

    def agregar_item(self, data):
        return self._admin.agregar_item(data)

    def actualizar_item(self, item_id, data):
        return self._admin.actualizar_item(item_id, data)
    
    def eliminar_item(self, item_id):
        return self._admin.eliminar_item(item_id)
    