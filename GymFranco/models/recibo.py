from datetime import date

class Recibo:
    def __init__(
        self,
        id_recibo: int,
        id_cliente: int,
        fecha: date,
        cantidad: float,
        pagado: bool = False,
    ):
        self.id_recibo = id_recibo
        self.id_cliente = id_cliente  # Guardamos SOLO el ID del cliente (BD-friendly)
        self.fecha = fecha
        self.cantidad = cantidad
        self.pagado = pagado

    def marcar_pagado(self):
        self.pagado = True

    def __str__(self):
        estado = "Pagado" if self.pagado else "Pendiente"
        return (
            f"Recibo({self.id_recibo} - ClienteID: {self.id_cliente}, "
            f"Fecha: {self.fecha}, Cantidad: {self.cantidad:.2f}€, {estado})"
        )
