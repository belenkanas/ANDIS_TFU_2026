from abc import ABC, abstractmethod

# Patrón Observer: define la interfaz base que todo observador debe cumplir
# cualquier clase que quiera "escuchar" cambios en un pedido debe implementar actualizar()
class PedidoObserver(ABC):
    @abstractmethod
    def actualizar(self, pedido) -> None:
        pass  # cada observador decide que hacer cuando recibe la notificacion


# observador 1: se encarga de notificar al cliente - PUC004
class NotificacionClienteObserver(PedidoObserver):
    def actualizar(self, pedido) -> None:
        from models.pedido import EstadoPedido  # hacemos import aca para evitar importacion circular
        if pedido.estado == EstadoPedido.LISTO:
            # solo actua cuando el pedido pasa a estado LISTO, ignora los demas cambios
            print(f"[NOTIFICACIÓN SMS] Pedido #{pedido.numero}: tu pedido está listo para retirar")


# observador 2: registra cada cambio de estado para auditoria
class RegistroAuditoriaObserver(PedidoObserver):
    def actualizar(self, pedido) -> None:
        # actua ante cualquier cambio, no solo cuando esta LISTO
        print(f"[AUDITORÍA] Pedido #{pedido.numero} → estado: {pedido.estado} | total: ${pedido.total}")


# Subject del patrón Observer: mantiene la lista de observadores y los notifica
# los observadores se suscriben aca y se llaman automaticamente ante cada cambio
class GestorObservadores:
    def __init__(self):
        self._observadores: list[PedidoObserver] = []  # lista de observadores suscriptos

    # agrega un observador a la lista
    def suscribir(self, observer: PedidoObserver) -> None:
        self._observadores.append(observer)

    # quita un observador de la lista
    def desuscribir(self, observer: PedidoObserver) -> None:
        self._observadores.remove(observer)

    # recorre todos los observadores y les avisa del cambio
    # cada uno decide internamente si le interesa actuar o no
    def notificar(self, pedido) -> None:
        for observer in self._observadores:
            observer.actualizar(pedido)