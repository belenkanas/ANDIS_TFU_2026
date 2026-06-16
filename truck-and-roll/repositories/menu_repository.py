from repositories.ILectorMenu import ILectorMenu
from repositories.IEscritorMenu import IEscritorMenu
from models.menu_item import MenuItem
from typing import List, Optional

# Patrón Repository: abstrae el acceso a datos del menu
# implementa ambas interfaces porque es quien tiene acceso completo a los datos
# ISP al implementar interfaces separadas, los servicios solo ven lo que necesitan
class MenuRepository(ILectorMenu, IEscritorMenu):
    def __init__(self):
        # almacenamiento en memoria: diccionario con id como clave
        self._items: dict = {
            1: MenuItem(id=1, nombre="Hamburguesa clásica", descripcion="Pan, carne, lechuga, tomate", precio=320.0),
            2: MenuItem(id=2, nombre="Papas fritas", descripcion="Porción grande", precio=150.0),
            3: MenuItem(id=3, nombre="Gaseosa", descripcion="Lata 350ml", precio=90.0),
            4: MenuItem(id=4, nombre="Hamburguesa doble", descripcion="Doble carne, cheddar y cebolla caramelizada", precio=450.0),
            5: MenuItem(id=5, nombre="Wrap de pollo", descripcion="Pollo grillado, lechuga, tomate y salsa", precio=380.0, disponible=False),
            6: MenuItem(id=6, nombre="Ensalada César", descripcion="Lechuga, pollo, croutones y aderezo César", precio=300.0, disponible=False),
            7: MenuItem(id=7, nombre="Agua mineral", descripcion="Botella 500ml", precio=70.0),
            8: MenuItem(id=8, nombre="Brownie con helado", descripcion="Brownie tibio con bocha de vainilla", precio=240.0, disponible=False),
        }
        self._next_id = max(self._items.keys(), default=0) + 1

    # filtra solo los items con disponible=True (los que ve el cajero)
    def listar_disponibles(self) -> List[MenuItem]:
        return [item for item in self._items.values() if item.disponible]

    # devuelve todos sin filtrar
    def listar_todos(self) -> List[MenuItem]:
        return list(self._items.values())

    # devuelve el item o None si no existe
    def buscar_por_id(self, item_id: int) -> Optional[MenuItem]:
        return self._items.get(item_id)

    # sobreescribe el item existente con los datos actualizados
    def guardar(self, item: MenuItem) -> MenuItem:
        self._items[item.id] = item
        return item

    # construye el MenuItem con el proximo id disponible y lo guarda. No se usan huecos de ids eliminados.
    def crear(self, nombre: str, descripcion: str, precio: float) -> MenuItem:
        nuevo = MenuItem(id=self._next_id, nombre=nombre, descripcion=descripcion, precio=precio)
        self._items[self._next_id] = nuevo
        self._next_id += 1
        return nuevo
    
    def eliminar(self, item_id: int) -> bool:
        if item_id in self._items:
            del self._items[item_id]
            return True
        return False