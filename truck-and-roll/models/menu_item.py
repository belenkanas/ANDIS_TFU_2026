from pydantic import BaseModel
from typing import Optional

# representa un item del menu
class MenuItem(BaseModel):
    id: int
    nombre: str
    descripcion: str
    precio: float
    disponible: bool = True     # por defecto todo item nuevo esta disponible

# datos que recibe la api al crear un nuevo item
# no tiene id ni disponible porque los asigna el sistema
class MenuItemCreate(BaseModel):
    nombre: str
    descripcion: str
    precio: float

# datos que recibe la api al modificar un item
# el dueño puede cambiar solo lo que necesita, por eso son todos opcionales
class MenuItemUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    precio: Optional[float] = None
    disponible: Optional[bool] = None