# GestionGym_PonceDeLeonFranco

Requisitos funcionales del aplicativo

1.1. Gestión de clientes

FR-01: El sistema permitirá dar de alta nuevos clientes, almacenando como mínimo: nombre, email y teléfono.


FR-02: El sistema validará que el teléfono solo contenga números (sin letras ni símbolos).


FR-03: El sistema validará que el correo electrónico contenga un carácter “@” y no empiece ni termine con él.


FR-04: El sistema permitirá listar todos los clientes registrados.


FR-05: El sistema permitirá consultar los datos de un cliente a partir de su identificador.


(Opcional futuro) FR-06: El sistema permitirá modificar los datos de un cliente.


(Opcional futuro) FR-07: El sistema permitirá eliminar un cliente, siempre que no existan datos dependientes.


- Gestión de aparatos

FR-08: El sistema permitirá dar de alta nuevos aparatos indicando: nombre, tipo (cardio, fuerza, etc.), estado (activo) e imagen asociada.


FR-09: El sistema permitirá listar todos los aparatos en una tabla, mostrando:


Imagen en miniatura,


Identificador,


Nombre,


Tipo,


Estado (Activo / Fuera de servicio),


Ocupación en tiempo real (LIBRE / OCUPADO).


FR-10: El sistema permitirá consultar si un aparato está ocupado en un momento dado en función de las sesiones registradas.


(Opcional futuro) FR-11: El sistema permitirá marcar un aparato como “fuera de servicio”.


Gestión de sesiones / reservas

FR-12: El sistema permitirá crear nuevas sesiones de entrenamiento, asociando un cliente y un aparato, para una fecha y hora de inicio.


FR-13: El sistema no permitirá crear una sesión si:


El cliente no existe.


El aparato no existe.


El aparato está marcado como no activo.


FR-14: El sistema permitirá listar todas las sesiones registradas.


FR-15: El sistema permitirá listar las sesiones de un día concreto.


(Opcional) FR-16: El sistema podrá comprobar solapamientos de horarios para evitar reservas simultáneas en el mismo aparato.


Gestión de recibos / pagos

FR-17: El sistema permitirá crear nuevos recibos asociados a un cliente, con:


Fecha,


Cantidad (por defecto, la cuota mensual del gimnasio),


Estado inicial “PENDIENTE”.


FR-18: El sistema almacenará los recibos en la base de datos para su consulta posterior.


FR-19: El sistema permitirá listar todos los recibos mostrando:


Cliente,


Fecha,


Cantidad,


Estado (PAGADO / PENDIENTE).


FR-20: El sistema permitirá marcar un recibo como pagado, actualizando su estado tanto en memoria como en la base de datos.


FR-21: El sistema permitirá filtrar y mostrar únicamente los recibos pendientes de pago (morosos).


FR-22: El sistema permitirá volver a mostrar todos los recibos (pagados y pendientes).


FR-23: El sistema permitirá listar los recibos de un cliente concreto.


Interfaz gráfica y persistencia

FR-24: El sistema dispondrá de una interfaz gráfica (GUI) en Tkinter, con:


Menú lateral (Clientes, Aparatos, Sesiones/Reservas, Recibos, Salir).


Área de contenido central que va cambiando de sección sin abrir nuevas ventanas.


FR-25: La aplicación se ejecutará en modo pantalla completa, permitiendo salir de este modo mediante la tecla ESC.


FR-26: Todos los datos (clientes, aparatos, sesiones y recibos) se almacenarán de forma persistente en una base de datos SQLite (gimnasio.db).



<img width="641" height="1076" alt="Diagrama_Gym" src="https://github.com/user-attachments/assets/f9382fb9-4c0d-4855-8560-066f03528be9" />


<img width="391" height="345" alt="Modelo_E-R_Gy," src="https://github.com/user-attachments/assets/b5dd74cb-56d2-442f-8081-fc8670372ec2" />



Normalización
1NF:


Todos los atributos son atómicos (no hay listas ni campos multivaluados).


2NF:


Todas las claves primarias son simples (un único atributo), por lo que no hay dependencias parciales.


3NF:


No hay dependencias transitivas de atributos no clave respecto a la clave primaria.


Cada atributo depende directamente de su clave (por ejemplo, en RECIBOS, fecha, cantidad y pagado dependen de id_recibo).


Por tanto, el modelo está en Tercera Forma Normal (3FN), que es lo que suelen pedir en trabajos de este tipo.






