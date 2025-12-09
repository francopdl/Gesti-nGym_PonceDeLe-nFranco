class Aparato:
    def __init__(
        self,
        id_aparato: int,
        nombre: str,
        tipo: str = "",
        activo: bool = True,
        imagen: str = ""
    ):
        self.id_aparato = id_aparato
        self.nombre = nombre
        self.tipo = tipo          # cardio, fuerza, etc.
        self.activo = activo      # disponible o no
        self.imagen = imagen      # ruta a la imagen

    def desactivar(self):
        self.activo = False

    def activar(self):
        self.activo = True

    def __str__(self):
        estado = "Activo" if self.activo else "Fuera de servicio"
        tipo = f" ({self.tipo})" if self.tipo else ""
        return f"Aparato({self.id_aparato} - {self.nombre}{tipo} - {estado})"
