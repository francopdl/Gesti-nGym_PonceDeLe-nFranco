class Cliente:
    def __init__(self, id_cliente: int, nombre: str, email: str, telefono: str):
        self.id_cliente = id_cliente
        self.nombre = nombre
        self.email = email
        self.telefono = telefono

    def __str__(self):
        return f"Cliente({self.id_cliente} - {self.nombre})"
