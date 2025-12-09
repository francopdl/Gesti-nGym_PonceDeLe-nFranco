from datetime import date, time, datetime, timedelta

from .cliente import Cliente
from .aparato import Aparato


class Sesion:
    DURACION_MINUTOS = 30

    def __init__(
        self,
        id_sesion: int,
        cliente: Cliente,
        aparato: Aparato,
        fecha: date,
        hora_inicio: time,
    ):
        self.id_sesion = id_sesion
        self.cliente = cliente
        self.aparato = aparato
        self.fecha = fecha
        self.hora_inicio = hora_inicio
        self.hora_fin = self._calcular_hora_fin()

    def _calcular_hora_fin(self) -> time:
        dt_inicio = datetime.combine(self.fecha, self.hora_inicio)
        dt_fin = dt_inicio + timedelta(minutes=self.DURACION_MINUTOS)
        return dt_fin.time()

    def __str__(self):
        return (
            f"Sesión({self.id_sesion} - Cliente: {self.cliente.nombre}, "
            f"Aparato: {self.aparato.nombre}, "
            f"{self.fecha} {self.hora_inicio.strftime('%H:%M')} - "
            f"{self.hora_fin.strftime('%H:%M')})"
        )
