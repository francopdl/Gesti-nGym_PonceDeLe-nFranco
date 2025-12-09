#  Requisitos Funcionales del Aplicativo

##  Gestión de Clientes

- **FR-01:** El sistema permitirá dar de alta nuevos clientes, almacenando como mínimo: nombre, email y teléfono.  
- **FR-02:** El sistema validará que el teléfono solo contenga números (sin letras ni símbolos).  
- **FR-03:** El sistema validará que el correo electrónico contenga un carácter **"@"** y que no empiece ni termine con él.  
- **FR-04:** El sistema permitirá listar todos los clientes registrados.  
- **FR-05:** El sistema permitirá consultar los datos de un cliente a partir de su identificador.  
- **FR-06 (Opcional futuro):** El sistema permitirá modificar los datos de un cliente.  
- **FR-07 (Opcional futuro):** El sistema permitirá eliminar un cliente, siempre que no existan datos dependientes.  

---

##  Gestión de Aparatos

- **FR-08:** El sistema permitirá dar de alta nuevos aparatos indicando: nombre, tipo (cardio, fuerza, etc.), estado (activo) e imagen asociada.  
- **FR-09:** El sistema permitirá listar todos los aparatos en una tabla, mostrando:
  - Imagen en miniatura  
  - Identificador  
  - Nombre  
  - Tipo  
  - Estado (Activo / Fuera de servicio)  
  - Ocupación en tiempo real (**LIBRE / OCUPADO**)  
- **FR-10:** El sistema permitirá consultar si un aparato está ocupado en un momento dado según las sesiones registradas.  
- **FR-11 (Opcional futuro):** El sistema permitirá marcar un aparato como “fuera de servicio”.  

---

##  Gestión de Sesiones / Reservas

- **FR-12:** El sistema permitirá crear nuevas sesiones asociando un cliente y un aparato, indicando fecha y hora de inicio.  
- **FR-13:** El sistema no permitirá crear una sesión si:
  - El cliente no existe  
  - El aparato no existe  
  - El aparato está inactivo  
- **FR-14:** El sistema permitirá listar todas las sesiones registradas.  
- **FR-15:** El sistema permitirá listar las sesiones de un día específico.  
- **FR-16 (Opcional):** El sistema podrá comprobar solapamientos de horarios para evitar reservas simultáneas en el mismo aparato.  

---

##  Gestión de Recibos / Pagos

- **FR-17:** El sistema permitirá crear nuevos recibos asociados a un cliente, incluyendo:
  - Fecha  
  - Cantidad (por defecto, la cuota mensual)  
  - Estado inicial: **PENDIENTE**  
- **FR-18:** El sistema almacenará los recibos en la base de datos.  
- **FR-19:** El sistema permitirá listar todos los recibos, mostrando:
  - Cliente  
  - Fecha  
  - Cantidad  
  - Estado (**PAGADO / PENDIENTE**)  
- **FR-20:** El sistema permitirá marcar un recibo como pagado.  
- **FR-21:** El sistema permitirá filtrar y mostrar solo los recibos pendientes (**morosos**).  
- **FR-22:** El sistema permitirá volver a mostrar todos los recibos.  
- **FR-23:** El sistema permitirá listar los recibos de un cliente concreto.  

---

##  Interfaz Gráfica y Persistencia

- **FR-24:** La aplicación dispondrá de una GUI en Tkinter con:
  - Menú lateral: *Clientes, Aparatos, Sesiones/Reservas, Recibos, Salir*.  
  - Área de contenido central que cambia de vista sin abrir nuevas ventanas.  
- **FR-25:** La aplicación se ejecutará en **pantalla completa**, pudiendo salir con **ESC**.  
- **FR-26:** Todos los datos (clientes, aparatos, sesiones, recibos) se almacenarán en **SQLite** (`gimnasio.db`).  

---

<img width="641" height="1076" alt="Diagrama_Gym" src="https://github.com/user-attachments/assets/1137bd20-8c7d-4c5e-b294-3a30b4699660" />

---

<img width="391" height="345" alt="Modelo_E-R_Gy," src="https://github.com/user-attachments/assets/462102b9-140e-4751-b343-68babae4fda9" />


---
#  Normalización del Modelo de Datos

El modelo se encuentra normalizado hasta **Tercera Forma Normal (3FN)**:

###  1NF — Primera Forma Normal
- Cada campo contiene **un único valor**, no listas ni valores repetidos dentro del mismo campo.  
  *(Ejemplo: “teléfono” contiene un solo número, no varios.)*
- Todas las filas son distinguibles y cada columna almacena siempre el mismo tipo de información.

###  2NF — Segunda Forma Normal
- Las claves primarias son simples.  
- No existen dependencias parciales.  

###  3NF — Tercera Forma Normal
- No hay dependencias transitivas entre atributos no clave.  
- Cada atributo depende directamente de su clave primaria.  

**Conclusión:**  
 El modelo cumple completamente con **3FN**, adecuado para aplicaciones reales y trabajos académicos.

