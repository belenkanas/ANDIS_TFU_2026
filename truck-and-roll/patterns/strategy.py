from abc import ABC, abstractmethod

# Patrón Strategy: define la interfaz base que toda estrategia de pago debe cumplir
# cada metodo de pago tiene su propia clase con su propia logica de procesamiento
class PagoStrategy(ABC):
    @abstractmethod
    def procesar(self, monto: float) -> dict:
        pass  # cada estrategia decide como procesa el pago


# estrategia 1: pago en efectivo
class EfectivoStrategy(PagoStrategy):
    # el efectivo se confirma de forma inmediata, no necesita pasarela
    def procesar(self, monto: float) -> dict:
        return {
            "metodo": "efectivo",
            "monto": monto,
            "estado": "confirmado",
            "mensaje": "Pago en efectivo registrado correctamente"
        }

# estrategia 2: pago con tarjeta
class TarjetaStrategy(PagoStrategy):
    def procesar(self, monto: float) -> dict:
        return {
            "metodo": "tarjeta",
            "monto": monto,
            "estado": "confirmado",
            "mensaje": "Pago con tarjeta procesado correctamente"
        }

# estrategia 3: pago con MercadoPago
class MercadoPagoStrategy(PagoStrategy):
    def procesar(self, monto: float) -> dict:
        return {
            "metodo": "mercadopago",
            "monto": monto,
            "estado": "confirmado",
            "mensaje": "Pago con MercadoPago procesado correctamente"
        }

# OCP - para agregar un nuevo metodo de pago por ej criptomonedas
# solo se agrega una nueva clase que herede de PagoStrategy y se registra aca
# no se modifica ninguna clase existente
def obtener_estrategia(metodo: str) -> PagoStrategy:
    estrategias = {
        "efectivo": EfectivoStrategy(),
        "tarjeta": TarjetaStrategy(),
        "mercadopago": MercadoPagoStrategy(),
    }
    if metodo not in estrategias:
        # si el cajero manda un metodo desconocido, el sistema lo rechaza
        raise ValueError(f"Método de pago '{metodo}' desconocido. Opciones: {list(estrategias.keys())}")
    return estrategias[metodo]