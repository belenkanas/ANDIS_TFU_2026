# Análisis y Diseño de Aplicaciones I 
# Trabajo Final de Unidad 5 - Equipo 5
# Truck & Roll

Backend REST para el sistema de gestión de food trucks, desarrollado en Python con FastAPI.

## Instalación

```bash
py -m pip install -r requirements.txt
```

## Ejecutar la API

Ubicados en el directorio ```ANDIS_TFU_2026\truck-and-roll```

```bash
py -m uvicorn main:app --reload
```

La API queda disponible en `http://localhost:8000`

Documentación: `http://localhost:8000/docs`

## Endpoints

### Root
- `GET /`

### Menú (`/menu`)
- `GET /menu/` - Ver menú disponible
- `POST /menu/` - Agregar ítem
- `PATCH /menu/{item_id}` - Modificar ítem
- `DELETE /menu/{item_id}` - Eliminar ítem

### Pedidos (`/pedidos`)
- `POST /pedidos/` - Registrar pedido
- `GET /pedidos/` - Ver todos los pedidos
- `GET /pedidos/cocina` - Ver pedidos `PENDIENTE` y `EN_PREPARACION`
- `GET /pedidos/mostrador` - Ver pedidos `LISTO`
- `GET /pedidos/{numero}` - Ver detalle de pedido
- `PATCH /pedidos/{numero}/estado` - Cambiar estado con payload
- `PATCH /pedidos/{numero}/preparacion` - Marcar `EN_PREPARACION`
- `PATCH /pedidos/{numero}/listo` - Marcar `LISTO`
- `PATCH /pedidos/{numero}/entregar` - Marcar `ENTREGADO`
