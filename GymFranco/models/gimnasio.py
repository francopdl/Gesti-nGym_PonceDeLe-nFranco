import sqlite3
from datetime import date, time, datetime
from typing import Dict, List, Optional

from .cliente import Cliente
from .aparato import Aparato
from .sesion import Sesion
from .recibo import Recibo


class Gimnasio:
    def __init__(self, nombre: str, cuota_mensual: float):
        self.nombre = nombre
        self.cuota_mensual = cuota_mensual

        self.clientes: Dict[int, Cliente] = {}
        self.aparatos: Dict[int, Aparato] = {}
        self.sesiones: Dict[int, Sesion] = {}
        self.recibos: Dict[int, Recibo] = {}

        self._next_id_cliente = 1
        self._next_id_aparato = 1
        self._next_id_sesion = 1
        self._next_id_recibo = 1

        # Conexión a SQLite
        self.conn = sqlite3.connect("gimnasio.db")
        self.conn.row_factory = sqlite3.Row

        self._init_db()
        self._cargar_desde_db()

    # -----------------------------------
    #   INICIALIZACIÓN BD
    # -----------------------------------
    def _init_db(self):
        cur = self.conn.cursor()

        # Tabla de clientes
        cur.execute("""
            CREATE TABLE IF NOT EXISTS clientes (
                id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre     TEXT NOT NULL,
                email      TEXT NOT NULL,
                telefono   TEXT NOT NULL
            );
        """)

        # Tabla de aparatos
        cur.execute("""
            CREATE TABLE IF NOT EXISTS aparatos (
                id_aparato INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre     TEXT NOT NULL,
                tipo       TEXT,
                activo     INTEGER NOT NULL DEFAULT 1,
                imagen     TEXT
            );
        """)

        # Tabla de sesiones
        cur.execute("""
            CREATE TABLE IF NOT EXISTS sesiones (
                id_sesion   INTEGER PRIMARY KEY AUTOINCREMENT,
                id_cliente  INTEGER NOT NULL,
                id_aparato  INTEGER NOT NULL,
                fecha       TEXT NOT NULL,
                hora_inicio TEXT NOT NULL,
                FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente),
                FOREIGN KEY (id_aparato) REFERENCES aparatos(id_aparato)
            );
        """)

        # Tabla de recibos
        cur.execute("""
            CREATE TABLE IF NOT EXISTS recibos (
                id_recibo   INTEGER PRIMARY KEY AUTOINCREMENT,
                id_cliente  INTEGER NOT NULL,
                fecha       TEXT NOT NULL,
                cantidad    REAL NOT NULL,
                pagado      INTEGER NOT NULL DEFAULT 0,
                FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente)
            );
        """)

        self.conn.commit()

    def _cargar_desde_db(self):
        cur = self.conn.cursor()

        # Clientes
        cur.execute("SELECT * FROM clientes")
        max_id = 0
        for row in cur.fetchall():
            cli = Cliente(row["id"], row["nombre"], row["email"], row["telefono"])
            self.clientes[cli.id_cliente] = cli
            max_id = max(max_id, cli.id_cliente)
        self._next_id_cliente = max_id + 1 if max_id > 0 else 1

        # Aparatos
        cur.execute("SELECT * FROM aparatos")
        max_id = 0
        for row in cur.fetchall():
            apa = Aparato(
                row["id"],
                row["nombre"],
                row["tipo"] or "",
                bool(row["activo"]),
                row["imagen"] or ""
            )
            self.aparatos[apa.id_aparato] = apa
            max_id = max(max_id, apa.id_aparato)
        self._next_id_aparato = max_id + 1 if max_id > 0 else 1

        # Sesiones
        cur.execute("SELECT * FROM sesiones")
        max_id = 0
        for row in cur.fetchall():
            cli = self.clientes.get(row["id_cliente"])
            apa = self.aparatos.get(row["id_aparato"])
            if cli and apa:
                f = datetime.strptime(row["fecha"], "%Y-%m-%d").date()
                h = datetime.strptime(row["hora_inicio"], "%H:%M").time()
                ses = Sesion(row["id"], cli, apa, f, h)
                self.sesiones[ses.id_sesion] = ses
                max_id = max(max_id, ses.id_sesion)
        self._next_id_sesion = max_id + 1 if max_id > 0 else 1

    # -----------------------------------
    #   CLIENTES
    # -----------------------------------
    def alta_cliente(self, nombre: str, email: str, telefono: str) -> Cliente:
        id_cliente = self._next_id_cliente
        cliente = Cliente(id_cliente, nombre, email, telefono)
        self.clientes[id_cliente] = cliente
        self._next_id_cliente += 1

        cur = self.conn.cursor()
        cur.execute(
            "INSERT INTO clientes (id, nombre, email, telefono) VALUES (?, ?, ?, ?)",
            (cliente.id_cliente, cliente.nombre, cliente.email, cliente.telefono)
        )
        self.conn.commit()
        return cliente

    def listar_clientes(self) -> List[Cliente]:
        return list(self.clientes.values())

    def buscar_cliente(self, id_cliente: int) -> Optional[Cliente]:
        return self.clientes.get(id_cliente)

    # -----------------------------------
    #   APARATOS
    # -----------------------------------
    def alta_aparato(self, nombre: str, tipo: str = "", imagen: str = "") -> Aparato:
        id_aparato = self._next_id_aparato
        aparato = Aparato(id_aparato, nombre, tipo, True, imagen)
        self.aparatos[id_aparato] = aparato
        self._next_id_aparato += 1

        cur = self.conn.cursor()
        cur.execute(
            "INSERT INTO aparatos (id, nombre, tipo, activo, imagen) VALUES (?, ?, ?, ?, ?)",
            (aparato.id_aparato, aparato.nombre, aparato.tipo, 1 if aparato.activo else 0, aparato.imagen)
        )
        self.conn.commit()
        return aparato

    def listar_aparatos(self) -> List[Aparato]:
        return list(self.aparatos.values())

    def buscar_aparato(self, id_aparato: int) -> Optional[Aparato]:
        return self.aparatos.get(id_aparato)

    def esta_aparato_ocupado(self, id_aparato: int, momento: Optional[datetime] = None) -> bool:
        if momento is None:
            momento = datetime.now()

        for s in self.sesiones.values():
            if s.aparato.id_aparato != id_aparato:
                continue
            if s.fecha != momento.date():
                continue
            if s.hora_inicio <= momento.time() < s.hora_fin:
                return True
        return False

    # -----------------------------------
    #   SESIONES
    # -----------------------------------
    def crear_sesion(
        self,
        id_cliente: int,
        id_aparato: int,
        fecha: date,
        hora_inicio: time,
    ) -> Sesion:
        cliente = self.buscar_cliente(id_cliente)
        aparato = self.buscar_aparato(id_aparato)

        if cliente is None:
            raise ValueError(f"No existe cliente con id {id_cliente}")
        if aparato is None:
            raise ValueError(f"No existe aparato con id {id_aparato}")
        if not aparato.activo:
            raise ValueError("El aparato no está disponible")

        id_sesion = self._next_id_sesion
        sesion = Sesion(id_sesion, cliente, aparato, fecha, hora_inicio)
        self.sesiones[id_sesion] = sesion
        self._next_id_sesion += 1

        cur = self.conn.cursor()
        cur.execute(
            "INSERT INTO sesiones (id, id_cliente, id_aparato, fecha, hora_inicio) "
            "VALUES (?, ?, ?, ?, ?)",
            (
                sesion.id_sesion,
                sesion.cliente.id_cliente,
                sesion.aparato.id_aparato,
                sesion.fecha.strftime("%Y-%m-%d"),
                sesion.hora_inicio.strftime("%H:%M"),
            )
        )
        self.conn.commit()
        return sesion

    def listar_sesiones(self) -> List[Sesion]:
        return list(self.sesiones.values())

    def listar_sesiones_por_dia(self, fecha: date) -> List[Sesion]:
        return [s for s in self.sesiones.values() if s.fecha == fecha]

    # -----------------------------------
    #   RECIBOS (solo memoria)
    # -----------------------------------
    # -----------------------------------
    #   RECIBOS (con BD)
    # -----------------------------------
    def crear_recibo(
            self,
            id_cliente: int,
            fecha: date,
            cantidad: Optional[float] = None,
            pagado: bool = False,
    ) -> Recibo:
        cliente = self.buscar_cliente(id_cliente)
        if cliente is None:
            raise ValueError(f"No existe cliente con id {id_cliente}")

        if cantidad is None:
            cantidad = self.cuota_mensual

        cur = self.conn.cursor()
        cur.execute(
            "INSERT INTO recibos (id_cliente, fecha, cantidad, pagado) "
            "VALUES (?, ?, ?, ?)",
            (id_cliente, fecha.isoformat(), cantidad, int(pagado))
        )
        self.conn.commit()

        id_recibo = cur.lastrowid

        recibo = Recibo(
            id_recibo=id_recibo,
            id_cliente=id_cliente,
            fecha=fecha.isoformat(),
            cantidad=cantidad,
            pagado=pagado
        )
        self.recibos[id_recibo] = recibo
        self._next_id_recibo = id_recibo + 1
        return recibo

    def listar_recibos(self) -> List[Recibo]:
        self.recibos.clear()
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM recibos")
        max_id = 0
        for row in cur.fetchall():
            r = Recibo(
                id_recibo=row["id_recibo"],
                id_cliente=row["id_cliente"],
                fecha=row["fecha"],
                cantidad=row["cantidad"],
                pagado=bool(row["pagado"])
            )
            self.recibos[r.id_recibo] = r
            max_id = max(max_id, r.id_recibo)
        self._next_id_recibo = max_id + 1 if max_id > 0 else 1
        return list(self.recibos.values())

    def listar_recibos_cliente(self, id_cliente: int) -> List[Recibo]:
        return [r for r in self.listar_recibos() if r.id_cliente == id_cliente]

    def marcar_recibo_pagado(self, id_recibo: int):
        recibo = self.recibos.get(id_recibo)
        if not recibo:
            return

        recibo.pagado = True
        cur = self.conn.cursor()
        cur.execute(
            "UPDATE recibos SET pagado = 1 WHERE id_recibo = ?",
            (id_recibo,)
        )
        self.conn.commit()
