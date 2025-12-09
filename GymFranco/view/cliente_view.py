def mostrar_menu_clientes():
    print("\n--- Gestión de clientes ---")
    print("1. Alta cliente")
    print("2. Listar clientes")
    print("3. Volver")
    opcion = input("Elige una opción: ")
    return opcion


def pedir_datos_cliente():
    nombre = input("Nombre: ")
    email = input("Email: ")
    telefono = input("Teléfono: ")
    return nombre, email, telefono


def mostrar_clientes(clientes):
    print("\nListado de clientes:")
    if not clientes:
        print("No hay clientes registrados.")
    else:
        for c in clientes:
            print(f"- {c.id_cliente}: {c.nombre} ({c.email}, {c.telefono})")
