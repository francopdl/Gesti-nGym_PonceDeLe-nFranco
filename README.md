# Requisitos Funcionales del Aplicativo
### Gestión de Clientes

FR-01: El sistema permitirá dar de alta nuevos clientes, almacenando como mínimo: nombre, email y teléfono.

FR-02: El sistema validará que el teléfono solo contenga números (sin letras ni símbolos).

FR-03: El sistema validará que el correo electrónico contenga un carácter "@" y no empiece ni termine con él.

FR-04: El sistema permitirá listar todos los clientes registrados.

FR-05: El sistema permitirá consultar los datos de un cliente a partir de su identificador.

FR-06 (Opcional futuro): El sistema permitirá modificar los datos de un cliente.

FR-07 (Opcional futuro): El sistema permitirá eliminar un cliente, siempre que no existan datos dependientes.

### Gestión de Aparatos

FR-08: El sistema permitirá dar de alta nuevos aparatos indicando: nombre, tipo (cardio, fuerza, etc.), estado (activo) e imagen asociada.

FR-09: El sistema permitirá listar todos los aparatos en una tabla, mostrando:

Imagen en miniatura

Identificador

Nombre

Tipo

Estado (Activo / Fuera de servicio)

Ocupación en tiempo real (LIBRE / OCUPADO)

FR-10: El sistema permitirá consultar si un aparato está ocupado en un momento dado en función de las sesiones registradas.

FR-11 (Opcional futuro): El sistema permitirá marcar un aparato como “fuera de servicio”.

### Gestión de Sesiones / Reservas

FR-12: El sistema permitirá crear nuevas sesiones de entrenamiento, asociando un cliente y un aparato, para una fecha y hora de inicio.

FR-13: El sistema no permitirá crear una sesión si:

El cliente no existe

El aparato no existe

El aparato está marcado como no activo

FR-14: El sistema permitirá listar todas las sesiones registradas.

FR-15: El sistema permitirá listar las sesiones de un día concreto.

FR-16 (Opcional): El sistema podrá comprobar solapamientos de horarios para evitar reservas simultáneas en el mismo aparato.

🔹 1.4. Gestión de Recibos / Pagos

FR-17: El sistema permitirá crear nuevos recibos asociados a un cliente, con:

Fecha

Cantidad (por defecto, la cuota mensual del gimnasio)

Estado inicial “PENDIENTE”

FR-18: El sistema almacenará los recibos en la base de datos para su consulta posterior.

FR-19: El sistema permitirá listar todos los recibos mostrando:

Cliente

Fecha

Cantidad

Estado (PAGADO / PENDIENTE)

FR-20: El sistema permitirá marcar un recibo como pagado, actualizando su estado tanto en memoria como en la base de datos.

FR-21: El sistema permitirá filtrar y mostrar únicamente los recibos pendientes de pago (morosos).

FR-22: El sistema permitirá volver a mostrar todos los recibos (pagados y pendientes).

FR-23: El sistema permitirá listar los recibos de un cliente concreto.

🔹 1.5. Interfaz Gráfica y Persistencia

FR-24: El sistema dispondrá de una interfaz gráfica (GUI) en Tkinter, con:

Menú lateral: Clientes, Aparatos, Sesiones/Reservas, Recibos, Salir.

Área de contenido central que cambia de sección sin abrir nuevas ventanas.

FR-25: La aplicación se ejecutará en modo pantalla completa, pudiendo salir mediante la tecla ESC.

FR-26: Todos los datos se almacenarán de forma persistente en una base de datos SQLite (gimnasio.db).

🧩 Normalización del Modelo de Datos

El modelo relacional del sistema cumple con:

✔ 1NF (Primera Forma Normal)

Todos los atributos son atómicos.

No existen listas ni atributos multivaluados.

✔ 2NF (Segunda Forma Normal)

Todas las claves primarias son simples (un solo atributo).

No existen dependencias parciales.

✔ 3NF (Tercera Forma Normal)

No existen dependencias transitivas de atributos no clave respecto a la clave primaria.

Cada atributo depende directamente de su clave.

Ejemplo: en RECIBOS, fecha, cantidad y pagado dependen únicamente de id_recibo.

👉 Conclusión: El modelo está correctamente normalizado hasta 3FN, adecuado para aplicaciones reales y para entregas académicas.
