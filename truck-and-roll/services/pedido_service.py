from repositories.ILectorPedido import ILectorPedido
from repositories.ILectorMenu import ILectorMenu
from models.pedido import Pedido, PedidoCreate, EstadoPedido, ItemPedido, TRANSICIONES_VALIDAS
from patterns.observer import GestorObservadores
from patterns.strategy import obtener_estrategia
from typing import List
from fastapi import HTTPException

class PedidoService:
    # DIP + ISP porque recibe interfaces, no clases concretas
    def __init__(self, pedido_repo: ILectorPedido, menu_repo: ILectorMenu, gestor: GestorObservadores):
        self._pedido_repo = pedido_repo  
        self._menu_repo = menu_repo   
        self._gestor = gestor  

    # Patrón Strategy: selecciona la clase de pago segun el metodo elegido por el cajero
    def registrar_pedido(self, data: PedidoCreate) -> Pedido:
        estrategia = obtener_estrategia(data.metodo_pago)
        items_pedido = []
        total = 0.0

        for item_data in data.items:
            # verifica que el item exista y este disponible antes de agregarlo
            menu_item = self._menu_repo.buscar_por_id(item_data["menu_item_id"])
            if not menu_item:
                raise HTTPException(status_code=404, detail=f"Ítem {item_data['menu_item_id']} no encontrado")
            if not menu_item.disponible:
                raise HTTPException(status_code=400, detail=f"'{menu_item.nombre}' no disponible")

            cantidad = item_data.get("cantidad", 1)
            total += menu_item.precio * cantidad
            items_pedido.append(ItemPedido(
                menu_item_id=menu_item.id,
                nombre=menu_item.nombre,
                cantidad=cantidad,
                precio_unitario=menu_item.precio,
            ))

        # Patrón Strategy: procesa el pago con la estrategia seleccionada
        resultado_pago = estrategia.procesar(total)

        # se arma el pedido con numero = 0 porque el repository le asigna el numero real
        pedido = Pedido(
            numero=0,
            items=items_pedido,
            total=total,
            metodo_pago=data.metodo_pago,
            resultado_pago=resultado_pago
        )
        pedido_guardado = self._pedido_repo.crear(pedido)

        # Patrón Observer: notifica a todos los usuarios que se creo un pedido
        self._gestor.notificar(pedido_guardado)
        return pedido_guardado

    # devuelve todos los pedidos para la cola del cocinero
    def listar_pedidos(self) -> List[Pedido]:
        return self._pedido_repo.listar()

    # cocina solo ve lo que esta por preparar o en preparacion
    def listar_pedidos_cocina(self) -> List[Pedido]:
        return [
            p for p in self._pedido_repo.listar()
            if p.estado in [EstadoPedido.PENDIENTE, EstadoPedido.EN_PREPARACION]
        ]

    # mostrador solo ve pedidos listos para entregar
    def listar_pedidos_mostrador(self) -> List[Pedido]:
        return [p for p in self._pedido_repo.listar() if p.estado == EstadoPedido.LISTO]

    def obtener_pedido(self, numero: int) -> Pedido:
        pedido = self._pedido_repo.buscar_por_numero(numero)
        if not pedido:
            raise HTTPException(status_code=404, detail="Pedido no encontrado")
        return pedido

    def cambiar_estado(self, numero: int, nuevo_estado: EstadoPedido) -> Pedido:
        pedido = self.obtener_pedido(numero)

        # Patrón State: valida que la transicion sea permitida segun TRANSICIONES_VALIDAS
        if nuevo_estado not in TRANSICIONES_VALIDAS[pedido.estado]:
            raise HTTPException(
                status_code=400,
                detail=f"Transición inválida: {pedido.estado} → {nuevo_estado}. "
                       f"Permitidas: {[e.value for e in TRANSICIONES_VALIDAS[pedido.estado]]}"
            )
        actualizado = pedido.model_copy(update={"estado": nuevo_estado})
        pedido_guardado = self._pedido_repo.guardar(actualizado)

        # Patrón Observer: notifica el cambio de estado a todos los usuarios
        # si el estado es LISTO, NotificacionClienteObserver dispara el SMS
        self._gestor.notificar(pedido_guardado)
        return pedido_guardado

    # PUC003 - llama a cambiar_estado con ENTREGADO
    # Patrón State valida que el pedido este en estado LISTO antes de permitirlo
    def entregar_pedido(self, numero: int) -> Pedido:
        return self.cambiar_estado(numero, EstadoPedido.ENTREGADO)

    # cocina marca el pedido como EN_PREPARACION (debe venir de PENDIENTE)
    def marcar_pedido_en_preparacion(self, numero: int) -> Pedido:
        return self.cambiar_estado(numero, EstadoPedido.EN_PREPARACION)

    # cocina marca el pedido como LISTO (debe venir de EN_PREPARACION)
    def marcar_pedido_listo(self, numero: int) -> Pedido:
        return self.cambiar_estado(numero, EstadoPedido.LISTO)