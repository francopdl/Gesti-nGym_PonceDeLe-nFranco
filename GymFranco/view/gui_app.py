import tkinter as tk
from tkinter import messagebox, filedialog
from datetime import datetime
from tkinter import ttk
from PIL import Image, ImageTk

from models.gimnasio import Gimnasio


class GymApp(tk.Tk):
    def __init__(self):
        super().__init__()

        # =========================
        # CONFIGURACIÓN GENERAL
        # =========================
        self.title("GymForTheMoment")

        # Pantalla completa siempre
        self.attributes("-fullscreen", True)
        # Salir de pantalla completa con ESC
        self.bind("<Escape>", lambda e: self.attributes("-fullscreen", False))

        # Colores (tema oscuro)
        self.color_bg = "#12121C"
        self.color_panel = "#1E1E2F"
        self.color_text = "#FFFFFF"
        self.color_accent = "#4A8CFF"

        self.configure(bg=self.color_bg)

        # =========================
        # MODELO PRINCIPAL
        # =========================
        self.gimnasio = Gimnasio("GymForTheMoment", cuota_mensual=50.0)

        # =========================
        # CONTENEDOR PRINCIPAL (IZQ: menú, DER: contenido)
        # =========================
        frame_principal = tk.Frame(self, bg=self.color_bg)
        frame_principal.pack(fill="both", expand=True)

        # -------- PANEL LATERAL IZQUIERDO --------
        sidebar = tk.Frame(frame_principal, bg=self.color_panel, width=260)
        sidebar.pack(side="left", fill="y")

        title_label = tk.Label(
            sidebar,
            text="GymForTheMoment",
            font=("Segoe UI", 18, "bold"),
            fg=self.color_text,
            bg=self.color_panel
        )
        title_label.pack(pady=40)

        botones = [
            ("Clientes", lambda: self.mostrar_frame("clientes")),
            ("Aparatos", lambda: self.mostrar_frame("aparatos")),
            ("Sesiones / Reservas", lambda: self.mostrar_frame("sesiones")),
            ("Recibos", lambda: self.mostrar_frame("recibos")),
            ("Salir", self.destroy),
        ]

        for texto, comando in botones:
            btn = tk.Button(
                sidebar,
                text=texto,
                font=("Segoe UI", 13),
                bg=self.color_accent,
                fg="white",
                bd=0,
                cursor="hand2",
                activebackground="#3576c4",
                activeforeground="white",
                command=comando
            )
            btn.pack(fill="x", padx=20, pady=10)

        # -------- CONTENEDOR DE CONTENIDO (DERECHA) --------
        self.content_frame = tk.Frame(frame_principal, bg=self.color_bg)
        self.content_frame.pack(side="right", expand=True, fill="both")

        # =========================
        # CREACIÓN DE FRAMES
        # (ClientesFrame, AparatosFrame, SesionesFrame, RecibosFrame
        # deben estar definidos en este mismo archivo gui_app.py)
        # =========================
        self.frames = {}

        self.frames["clientes"] = ClientesFrame(self.content_frame, self.gimnasio, self)
        self.frames["aparatos"] = AparatosFrame(self.content_frame, self.gimnasio, self)
        self.frames["sesiones"] = SesionesFrame(self.content_frame, self.gimnasio, self)
        self.frames["recibos"] = RecibosFrame(self.content_frame, self.gimnasio, self)

        # Todos los frames se añaden, pero luego se ocultan
        for frame in self.frames.values():
            frame.pack(fill="both", expand=True)
            frame.pack_forget()

        # Mostrar pantalla inicial
        self.mostrar_frame("clientes")

    # =========================
    # CAMBIO DE SECCIÓN
    # =========================
    def mostrar_frame(self, nombre_frame: str):
        # Ocultar todos
        for f in self.frames.values():
            f.pack_forget()

        # Mostrar solo el que toca
        frame = self.frames[nombre_frame]
        frame.pack(fill="both", expand=True)



# ==============================
#    FRAME: CLIENTES
# ==============================

class ClientesFrame(tk.Frame):
    def __init__(self, parent, gimnasio: Gimnasio, app: GymApp):
        super().__init__(parent, bg=app.color_bg)
        self.gimnasio = gimnasio
        self.app = app

        panel = tk.Frame(self, bg=app.color_panel, padx=20, pady=20)
        panel.pack(fill="both", expand=True, padx=20, pady=20)

        tk.Label(
            panel,
            text="Gestión de clientes",
            font=("Segoe UI", 16, "bold"),
            fg=app.color_text,
            bg=app.color_panel
        ).grid(row=0, column=0, columnspan=2, pady=(0, 10), sticky="w")

        tk.Label(panel, text="Nombre:", fg=app.color_text, bg=app.color_panel).grid(
            row=1, column=0, sticky="e", padx=5, pady=5
        )
        self.entry_nombre = tk.Entry(panel, width=30, font=("Segoe UI", 11))
        self.entry_nombre.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        tk.Label(panel, text="Email:", fg=app.color_text, bg=app.color_panel).grid(
            row=2, column=0, sticky="e", padx=5, pady=5
        )
        self.entry_email = tk.Entry(panel, width=30, font=("Segoe UI", 11))
        self.entry_email.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        tk.Label(panel, text="Teléfono:", fg=app.color_text, bg=app.color_panel).grid(
            row=3, column=0, sticky="e", padx=5, pady=5
        )
        self.entry_telefono = tk.Entry(panel, width=30, font=("Segoe UI", 11))
        self.entry_telefono.grid(row=3, column=1, padx=5, pady=5, sticky="w")

        btn_alta = tk.Button(
            panel,
            text="Dar de alta cliente",
            font=("Segoe UI", 11),
            bg=app.color_accent,
            fg="white",
            bd=0,
            activebackground="#3576c4",
            activeforeground="white",
            cursor="hand2",
            command=self.alta_cliente
        )
        btn_alta.grid(row=4, column=0, columnspan=2, pady=10, sticky="w")

        tk.Label(
            panel,
            text="Listado de clientes",
            font=("Segoe UI", 13, "bold"),
            fg=app.color_text,
            bg=app.color_panel
        ).grid(row=5, column=0, columnspan=2, pady=(15, 5), sticky="w")

        self.listbox_clientes = tk.Listbox(panel, width=60, height=12, font=("Consolas", 10))
        self.listbox_clientes.grid(row=6, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

        panel.rowconfigure(6, weight=1)
        panel.columnconfigure(1, weight=1)

        btn_refrescar = tk.Button(
            panel,
            text="Refrescar lista",
            font=("Segoe UI", 10),
            bg="#3b3b52",
            fg="white",
            bd=0,
            activebackground="#52527a",
            activeforeground="white",
            cursor="hand2",
            command=self.refrescar
        )
        btn_refrescar.grid(row=7, column=0, columnspan=2, pady=5, sticky="e")

        self.refrescar()

    def alta_cliente(self):
        nombre = self.entry_nombre.get().strip()
        email = self.entry_email.get().strip()
        telefono = self.entry_telefono.get().strip()

        # 1) Campos obligatorios
        if not nombre or not email or not telefono:
            messagebox.showwarning("Datos incompletos", "Rellena todos los campos.")
            return

        # 2) Validar teléfono (solo números)
        if not telefono.isdigit():
            messagebox.showerror(
                "Teléfono no válido",
                "El teléfono solo puede contener números (sin espacios ni letras)."
            )
            return

        # 3) Validar email muy básico: debe contener una @
        if "@" not in email or email.startswith("@") or email.endswith("@"):
            messagebox.showerror(
                "Email no válido",
                "Introduce un email correcto que contenga un '@'."
            )
            return

        # Si pasa todas las validaciones, damos de alta
        cliente = self.gimnasio.alta_cliente(nombre, email, telefono)
        messagebox.showinfo("Éxito", f"Cliente creado: {cliente.nombre}")

        # Limpiar campos
        self.entry_nombre.delete(0, tk.END)
        self.entry_email.delete(0, tk.END)
        self.entry_telefono.delete(0, tk.END)

        self.refrescar()

    def refrescar(self):
        self.listbox_clientes.delete(0, tk.END)
        for c in self.gimnasio.listar_clientes():
            self.listbox_clientes.insert(
                tk.END,
                f"{c.id_cliente:3d} | {c.nombre:20s} | {c.email:25s} | {c.telefono}"
            )



#    FRAME: APARATOS


class AparatosFrame(tk.Frame):
    def __init__(self, parent, gimnasio: Gimnasio, app: GymApp):
        super().__init__(parent, bg=app.color_bg)
        self.gimnasio = gimnasio
        self.app = app

        self.imagen_path = ""
        self.preview_image = None
        self.imagenes_cache = {}  # id_aparato -> miniatura (PhotoImage)

        # ====== CONTENEDOR PRINCIPAL ======
        panel = tk.Frame(self, bg=app.color_panel, padx=20, pady=20)
        panel.pack(fill="both", expand=True, padx=20, pady=20)

        # Layout: columnas 0-1 formulario, 2 listado
        panel.columnconfigure(0, weight=0)
        panel.columnconfigure(1, weight=0)
        panel.columnconfigure(2, weight=1)
        panel.rowconfigure(2, weight=1)

        # ====== TÍTULO ======
        tk.Label(
            panel,
            text="Gestión de aparatos",
            font=("Segoe UI", 18, "bold"),
            fg=app.color_text,
            bg=app.color_panel
        ).grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 15))

        # ====== IZQUIERDA: FORMULARIO + PREVIEW ======
        left_frame = tk.Frame(panel, bg=app.color_panel)
        left_frame.grid(row=1, column=0, rowspan=3, columnspan=2, sticky="nw", padx=(0, 25))

        tk.Label(left_frame, text="Nombre:", fg=app.color_text, bg=app.color_panel).grid(
            row=0, column=0, sticky="e", padx=5, pady=5
        )
        self.entry_nombre = tk.Entry(left_frame, width=28, font=("Segoe UI", 11))
        self.entry_nombre.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        tk.Label(left_frame, text="Tipo:", fg=app.color_text, bg=app.color_panel).grid(
            row=1, column=0, sticky="e", padx=5, pady=5
        )
        self.entry_tipo = tk.Entry(left_frame, width=28, font=("Segoe UI", 11))
        self.entry_tipo.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        tk.Label(left_frame, text="Imagen:", fg=app.color_text, bg=app.color_panel).grid(
            row=2, column=0, sticky="e", padx=5, pady=5
        )
        btn_img = tk.Button(
            left_frame,
            text="Seleccionar...",
            font=("Segoe UI", 10),
            bg=app.color_accent,
            fg="white",
            bd=0,
            activebackground="#3576c4",
            activeforeground="white",
            cursor="hand2",
            command=self.seleccionar_imagen
        )
        btn_img.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        self.label_preview = tk.Label(
            left_frame,
            text="Sin imagen",
            fg=app.color_text,
            bg="#181824",
            width=22,
            height=10,
            relief="sunken"
        )
        self.label_preview.grid(row=3, column=0, columnspan=2, pady=(10, 10))

        btn_alta = tk.Button(
            left_frame,
            text="Dar de alta aparato",
            font=("Segoe UI", 11, "bold"),
            bg=app.color_accent,
            fg="white",
            bd=0,
            activebackground="#3576c4",
            activeforeground="white",
            cursor="hand2",
            command=self.alta_aparato
        )
        btn_alta.grid(row=4, column=0, columnspan=2, pady=(5, 10), sticky="ew")

        # ====== DERECHA: LISTADO CON IMÁGENES (Treeview) ======
        tk.Label(
            panel,
            text="Listado de aparatos",
            font=("Segoe UI", 14, "bold"),
            fg=app.color_text,
            bg=app.color_panel
        ).grid(row=1, column=2, sticky="w", pady=(0, 5))

        list_frame = tk.Frame(panel, bg=app.color_panel)
        list_frame.grid(row=2, column=2, sticky="nsew")
        list_frame.rowconfigure(0, weight=1)
        list_frame.columnconfigure(0, weight=1)

        # Estilo para dar más altura a cada fila
        style = ttk.Style()
        style.configure(
            "Aparatos.Treeview",
            rowheight=56,
            font=("Segoe UI", 11)
        )
        style.configure(
            "Aparatos.Treeview.Heading",
            font=("Segoe UI", 11, "bold")
        )

        # Columna árbol (#0) = imagen + "id | nombre"
        self.tree_aparatos = ttk.Treeview(
            list_frame,
            columns=("tipo", "estado", "ocup"),
            show="tree headings",        # columna árbol + cabeceras
            height=18,
            style="Aparatos.Treeview"
        )

        # Encabezados
        self.tree_aparatos.heading("#0", text="ID | Nombre")
        self.tree_aparatos.heading("tipo", text="Tipo")
        self.tree_aparatos.heading("estado", text="Estado")
        self.tree_aparatos.heading("ocup", text="Ocupación")

        # Anchos columnas
        self.tree_aparatos.column("#0", width=260, anchor="w", stretch=True)
        self.tree_aparatos.column("tipo", width=130, anchor="center", stretch=True)
        self.tree_aparatos.column("estado", width=140, anchor="center", stretch=True)
        self.tree_aparatos.column("ocup", width=110, anchor="center", stretch=False)

        scroll_y = ttk.Scrollbar(list_frame, orient="vertical", command=self.tree_aparatos.yview)
        self.tree_aparatos.configure(yscrollcommand=scroll_y.set)

        self.tree_aparatos.grid(row=0, column=0, sticky="nsew")
        scroll_y.grid(row=0, column=1, sticky="ns")

        self.tree_aparatos.bind("<<TreeviewSelect>>", self.mostrar_imagen_aparato)

        btn_refrescar = tk.Button(
            panel,
            text="Refrescar lista",
            font=("Segoe UI", 10),
            bg="#3b3b52",
            fg="white",
            bd=0,
            activebackground="#52527a",
            activeforeground="white",
            cursor="hand2",
            command=self.refrescar
        )
        btn_refrescar.grid(row=3, column=2, pady=(8, 0), sticky="e")

        self.refrescar()

    # ---------- MÉTODOS AUXILIARES ----------

    def seleccionar_imagen(self):
        ruta = filedialog.askopenfilename(
            title="Seleccionar imagen",
            filetypes=[("Imágenes", "*.png;*.jpg;*.jpeg;*.gif"), ("Todos los archivos", "*.*")]
        )
        if ruta:
            self.imagen_path = ruta
            try:
                img = Image.open(ruta)
                img = img.resize((150, 150))
                img_tk = ImageTk.PhotoImage(img)

                self.preview_image = img_tk
                self.label_preview.config(image=self.preview_image, text="")
            except Exception as e:
                print("Error cargando imagen:", e)
                self.preview_image = None
                self.label_preview.config(text="(No previsualizable)", image="")

    def alta_aparato(self):
        nombre = self.entry_nombre.get().strip()
        tipo = self.entry_tipo.get().strip()

        if not nombre:
            messagebox.showwarning("Datos incompletos", "El nombre es obligatorio.")
            return

        aparato = self.gimnasio.alta_aparato(nombre, tipo, self.imagen_path)
        messagebox.showinfo("Éxito", f"Aparato creado: {aparato.nombre}")

        # Limpiar formulario
        self.entry_nombre.delete(0, tk.END)
        self.entry_tipo.delete(0, tk.END)
        self.imagen_path = ""
        self.label_preview.config(text="Sin imagen", image="")
        self.preview_image = None

        self.refrescar()

    def _get_miniatura(self, id_aparato: int, ruta: str):
        """Devuelve una miniatura para la lista (cacheada)."""
        if not ruta:
            return None

        if id_aparato in self.imagenes_cache:
            return self.imagenes_cache[id_aparato]

        try:
            img = Image.open(ruta)
            img = img.resize((32, 32))  # miniatura pequeña → no se pisan
            img_tk = ImageTk.PhotoImage(img)
            self.imagenes_cache[id_aparato] = img_tk
            return img_tk
        except Exception as e:
            print(f"Error cargando miniatura para aparato {id_aparato}: {e}")
            return None

    def refrescar(self):
        from datetime import datetime
        ahora = datetime.now()

        # Limpiar el tree
        for item in self.tree_aparatos.get_children():
            self.tree_aparatos.delete(item)

        # Volver a cargar aparatos
        for a in self.gimnasio.listar_aparatos():
            tipo_txt = a.tipo if a.tipo else "-"
            estado = "Activo" if a.activo else "Fuera de servicio"
            ocupado = self.gimnasio.esta_aparato_ocupado(a.id_aparato, ahora)
            estado_ocup = "[OCUPADO]" if ocupado else "[LIBRE]"

            mini = self._get_miniatura(a.id_aparato, a.imagen)
            texto = f"{a.id_aparato} | {a.nombre}"

            # OJO: aquí van SOLO kwargs válidos: text, image, values
            self.tree_aparatos.insert(
                "",
                "end",
                iid=str(a.id_aparato),
                text=texto,
                image=mini if mini is not None else "",
                values=(tipo_txt, estado, estado_ocup)
            )

    def mostrar_imagen_aparato(self, event):
        seleccion = self.tree_aparatos.selection()
        if not seleccion:
            return

        iid = seleccion[0]
        try:
            id_aparato = int(iid)
        except ValueError:
            return

        aparato = self.gimnasio.buscar_aparato(id_aparato)
        if not aparato or not aparato.imagen:
            self.label_preview.config(text="Sin imagen", image="")
            self.preview_image = None
            return

        ruta = aparato.imagen
        try:
            img = Image.open(ruta)
            img = img.resize((200, 200))
            img_tk = ImageTk.PhotoImage(img)

            self.preview_image = img_tk
            self.label_preview.config(image=self.preview_image, text="")
        except Exception as e:
            print("Error cargando imagen grande del aparato:", e)
            self.label_preview.config(text="(No previsualizable)", image="")
            self.preview_image = None





# ==============================
#    FRAME: SESIONES
# ==============================

class SesionesFrame(tk.Frame):
    def __init__(self, parent, gimnasio: Gimnasio, app: GymApp):
        super().__init__(parent, bg=app.color_bg)
        self.gimnasio = gimnasio
        self.app = app

        panel = tk.Frame(self, bg=app.color_panel, padx=20, pady=20)
        panel.pack(fill="both", expand=True, padx=20, pady=20)

        tk.Label(
            panel,
            text="Gestión de sesiones / reservas",
            font=("Segoe UI", 16, "bold"),
            fg=app.color_text,
            bg=app.color_panel
        ).grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 10))

        tk.Label(panel, text="ID Cliente:", fg=app.color_text, bg=app.color_panel).grid(
            row=1, column=0, sticky="e", padx=5, pady=5
        )
        self.entry_id_cliente = tk.Entry(panel, width=8, font=("Segoe UI", 11))
        self.entry_id_cliente.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        tk.Label(panel, text="ID Aparato:", fg=app.color_text, bg=app.color_panel).grid(
            row=2, column=0, sticky="e", padx=5, pady=5
        )
        self.entry_id_aparato = tk.Entry(panel, width=8, font=("Segoe UI", 11))
        self.entry_id_aparato.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        tk.Label(panel, text="Fecha (dd/mm/aaaa):", fg=app.color_text, bg=app.color_panel).grid(
            row=3, column=0, sticky="e", padx=5, pady=5
        )
        self.entry_fecha = tk.Entry(panel, width=12, font=("Segoe UI", 11))
        self.entry_fecha.grid(row=3, column=1, padx=5, pady=5, sticky="w")

        tk.Label(panel, text="Hora inicio (HH:MM):", fg=app.color_text, bg=app.color_panel).grid(
            row=4, column=0, sticky="e", padx=5, pady=5
        )
        self.entry_hora = tk.Entry(panel, width=10, font=("Segoe UI", 11))
        self.entry_hora.grid(row=4, column=1, padx=5, pady=5, sticky="w")

        btn_crear = tk.Button(
            panel,
            text="Crear sesión",
            font=("Segoe UI", 11),
            bg=app.color_accent,
            fg="white",
            bd=0,
            activebackground="#3576c4",
            activeforeground="white",
            cursor="hand2",
            command=self.crear_sesion
        )
        btn_crear.grid(row=5, column=0, columnspan=2, pady=10, sticky="w")

        tk.Label(
            panel,
            text="Ver sesiones por día",
            font=("Segoe UI", 13, "bold"),
            fg=app.color_text,
            bg=app.color_panel
        ).grid(row=6, column=0, columnspan=2, pady=(15, 5), sticky="w")

        tk.Label(panel, text="Fecha (dd/mm/aaaa):", fg=app.color_text, bg=app.color_panel).grid(
            row=7, column=0, sticky="e", padx=5, pady=5
        )
        self.entry_fecha_cons = tk.Entry(panel, width=12, font=("Segoe UI", 11))
        self.entry_fecha_cons.grid(row=7, column=1, padx=5, pady=5, sticky="w")

        btn_ver_dia = tk.Button(
            panel,
            text="Mostrar sesiones del día",
            font=("Segoe UI", 10),
            bg="#3b3b52",
            fg="white",
            bd=0,
            activebackground="#52527a",
            activeforeground="white",
            cursor="hand2",
            command=self.mostrar_sesiones_dia
        )
        btn_ver_dia.grid(row=8, column=0, columnspan=2, pady=5, sticky="w")

        tk.Label(
            panel,
            text="Todas las sesiones",
            font=("Segoe UI", 13, "bold"),
            fg=app.color_text,
            bg=app.color_panel
        ).grid(row=1, column=2, pady=(0, 5), sticky="w", padx=(30, 5))

        self.listbox_sesiones = tk.Listbox(panel, width=60, height=15, font=("Consolas", 10))
        self.listbox_sesiones.grid(row=2, column=2, rowspan=6, padx=(30, 5), pady=5, sticky="nsew")

        panel.columnconfigure(2, weight=1)
        panel.rowconfigure(2, weight=1)

        btn_refrescar = tk.Button(
            panel,
            text="Refrescar todas",
            font=("Segoe UI", 10),
            bg="#3b3b52",
            fg="white",
            bd=0,
            activebackground="#52527a",
            activeforeground="white",
            cursor="hand2",
            command=self.refrescar
        )
        btn_refrescar.grid(row=8, column=2, pady=5, sticky="e")

        self.refrescar()

    def crear_sesion(self):
        id_cliente_str = self.entry_id_cliente.get().strip()
        id_aparato_str = self.entry_id_aparato.get().strip()
        fecha_str = self.entry_fecha.get().strip()
        hora_str = self.entry_hora.get().strip()

        try:
            id_cliente = int(id_cliente_str)
            id_aparato = int(id_aparato_str)
            fecha = datetime.strptime(fecha_str, "%d/%m/%Y").date()
            hora = datetime.strptime(hora_str, "%H:%M").time()

            sesion = self.gimnasio.crear_sesion(id_cliente, id_aparato, fecha, hora)
            messagebox.showinfo("Éxito", f"Sesión creada (ID {sesion.id_sesion})")
            self.refrescar()

        except ValueError as e:
            messagebox.showerror("Error", f"Error al crear la sesión:\n{e}")

    def mostrar_sesiones_dia(self):
        fecha_str = self.entry_fecha_cons.get().strip()
        try:
            fecha = datetime.strptime(fecha_str, "%d/%m/%Y").date()
        except ValueError:
            messagebox.showerror("Error", "Fecha no válida. Usa dd/mm/aaaa.")
            return

        sesiones = self.gimnasio.listar_sesiones_por_dia(fecha)
        self.listbox_sesiones.delete(0, tk.END)
        if not sesiones:
            self.listbox_sesiones.insert(tk.END, "No hay sesiones en ese día.")
        else:
            for s in sesiones:
                self.listbox_sesiones.insert(
                    tk.END,
                    f"{s.id_sesion:3d} | {s.fecha} {s.hora_inicio.strftime('%H:%M')}-"
                    f"{s.hora_fin.strftime('%H:%M')} | {s.cliente.nombre:15s} | {s.aparato.nombre}"
                )

    def refrescar(self):
        self.listbox_sesiones.delete(0, tk.END)
        for s in self.gimnasio.listar_sesiones():
            self.listbox_sesiones.insert(
                tk.END,
                f"{s.id_sesion:3d} | {s.fecha} {s.hora_inicio.strftime('%H:%M')}-"
                f"{s.hora_fin.strftime('%H:%M')} | {s.cliente.nombre:15s} | {s.aparato.nombre}"
            )


# ==============================
#    FRAME: RECIBOS
# ==============================

class RecibosFrame(tk.Frame):
    def __init__(self, parent, gimnasio: Gimnasio, app: GymApp):
        super().__init__(parent, bg=app.color_bg)
        self.gimnasio = gimnasio
        self.app = app

        self.modo_morosos = False  # para saber si estoy filtrando morosos o no

        panel = tk.Frame(self, bg=app.color_panel, padx=20, pady=20)
        panel.pack(fill="both", expand=True)

        tk.Label(
            panel,
            text="Gestión de recibos",
            font=("Segoe UI", 18, "bold"),
            fg=app.color_text,
            bg=app.color_panel
        ).pack(pady=(0, 15))

        # ----------- BOTONES SUPERIORES -----------
        botones_frame = tk.Frame(panel, bg=app.color_panel)
        botones_frame.pack(fill="x", pady=10)

        tk.Button(
            botones_frame,
            text="Crear nuevo recibo",
            bg=app.color_accent,
            fg="white",
            font=("Segoe UI", 11),
            bd=0,
            cursor="hand2",
            command=self.crear_recibo
        ).pack(side="left", padx=5)

        tk.Button(
            botones_frame,
            text="Marcar como pagado",
            bg="#4CAF50",
            fg="white",
            font=("Segoe UI", 11),
            bd=0,
            cursor="hand2",
            command=self.marcar_pagado
        ).pack(side="left", padx=5)

        tk.Button(
            botones_frame,
            text="Ver morosos",
            bg="#D9534F",
            fg="white",
            font=("Segoe UI", 11),
            bd=0,
            cursor="hand2",
            command=self.mostrar_morosos
        ).pack(side="right", padx=5)

        tk.Button(
            botones_frame,
            text="Ver todos",
            bg="#5A5A7A",
            fg="white",
            font=("Segoe UI", 11),
            bd=0,
            cursor="hand2",
            command=self.mostrar_todos
        ).pack(side="right", padx=5)

        # ----------- TABLA DE RECIBOS -----------
        self.tree = ttk.Treeview(
            panel,
            columns=("cliente", "fecha", "cantidad", "estado"),
            show="headings",
            height=20
        )

        self.tree.heading("cliente", text="Cliente")
        self.tree.heading("fecha", text="Fecha")
        self.tree.heading("cantidad", text="Cantidad (€)")
        self.tree.heading("estado", text="Estado")

        self.tree.column("cliente", width=200)
        self.tree.column("fecha", width=120)
        self.tree.column("cantidad", width=120)
        self.tree.column("estado", width=120)

        self.tree.pack(fill="both", expand=True)

        scroll = ttk.Scrollbar(panel, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll.set)
        scroll.pack(side="right", fill="y")

        self.refrescar()

    # =================================
    # CREAR RECIBO
    # =================================
    def crear_recibo(self):
        # Recibo simple: usa la cuota mensual del gimnasio
        from datetime import date

        # Debe tener al menos 1 cliente
        if len(self.gimnasio.clientes) == 0:
            messagebox.showwarning("Sin clientes", "Primero debes crear un cliente.")
            return

        # Seleccionar cliente por ID
        import tkinter.simpledialog as sd
        id_cliente = sd.askinteger("Nuevo recibo", "ID del cliente:")

        if id_cliente not in self.gimnasio.clientes:
            messagebox.showerror("Error", "Cliente no encontrado.")
            return

        cliente = self.gimnasio.clientes[id_cliente]

        recibo = self.gimnasio.crear_recibo(
            id_cliente=cliente.id_cliente,
            fecha=date.today(),
            cantidad=self.gimnasio.cuota_mensual,
            pagado=False
        )

        messagebox.showinfo("OK", f"Recibo creado para {cliente.nombre} por {recibo.cantidad}€")
        self.refrescar()

    # =================================
    # MARCAR RECIBO COMO PAGADO
    # =================================
    def marcar_pagado(self):
        seleccionado = self.tree.selection()

        if not seleccionado:
            messagebox.showwarning("Atención", "Debes seleccionar un recibo.")
            return

        iid = seleccionado[0]

        try:
            id_recibo = int(iid)
        except ValueError:
            messagebox.showerror("Error", "ID de recibo no válido.")
            return

        recibo = self.gimnasio.recibos.get(id_recibo)

        if not recibo:
            messagebox.showerror("Error", "Recibo no encontrado.")
            return

        if recibo.pagado:
            messagebox.showinfo("Información", "Este recibo ya está pagado.")
            return

        # ✅ Actualizamos en el modelo + BD
        self.gimnasio.marcar_recibo_pagado(id_recibo)

        messagebox.showinfo("OK", f"Recibo #{id_recibo} marcado como pagado.")
        self.refrescar()

    # =================================
    # MOSTRAR SOLO MOROSOS
    # =================================
    def mostrar_morosos(self):
        self.modo_morosos = True
        self.refrescar()

    # =================================
    # MOSTRAR TODOS
    # =================================
    def mostrar_todos(self):
        self.modo_morosos = False
        self.refrescar()

    # =================================
    # RECARGAR LA TABLA
    # =================================
    def refrescar(self):
        # Limpiar
        for item in self.tree.get_children():
            self.tree.delete(item)

        for r in self.gimnasio.listar_recibos():

            if self.modo_morosos and r.pagado:
                continue  # solo mostrar impagos

            cliente = self.gimnasio.clientes.get(r.id_cliente)
            nombre = cliente.nombre if cliente else "(Desconocido)"

            estado = "PAGADO" if r.pagado else "PENDIENTE"

            self.tree.insert(
                "",
                "end",
                iid=str(r.id_recibo),
                values=(nombre, r.fecha, f"{r.cantidad}€", estado)
            )

