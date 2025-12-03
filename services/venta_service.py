#!/usr/bin/env python3
from typing import List, Optional, Tuple
from datetime import datetime

from models.venta import Venta
from nexus_core.db import MySQLDatabase


class VentaService:
    def __init__(self, db: MySQLDatabase):
        self.db = db

    def listar(self) -> List[Venta]:
        rows = self.db.execute(
            """
            SELECT v.id, v.cliente, v.total, v.fecha, u.nombre
            FROM ventas v
            LEFT JOIN usuarios u ON v.usuario_id = u.id
            ORDER BY v.fecha DESC
            """
        )
        return [Venta.from_row(r) for r in rows] if rows else []

    def buscar(self, texto: str) -> List[Venta]:
        rows = self.db.execute(
            """
            SELECT v.id, v.cliente, v.total, v.fecha, u.nombre
            FROM ventas v
            LEFT JOIN usuarios u ON v.usuario_id = u.id
            WHERE v.cliente LIKE %s OR v.id LIKE %s
            ORDER BY v.fecha DESC
            """,
            (f"%{texto}%", f"%{texto}%"),
        )
        return [Venta.from_row(r) for r in rows] if rows else []

    def filtrar_por_fechas(self, desde: str, hasta: str) -> List[Venta]:
        rows = self.db.execute(
            """
            SELECT v.id, v.cliente, v.total, v.fecha, u.nombre
            FROM ventas v
            LEFT JOIN usuarios u ON v.usuario_id = u.id
            WHERE DATE(v.fecha) BETWEEN %s AND %s
            ORDER BY v.fecha DESC
            """,
            (desde, hasta),
        )
        return [Venta.from_row(r) for r in rows] if rows else []

    def crear(self, cliente: str, total: float, usuario_id: Optional[int]) -> int:
        return int(
            self.db.execute(
                "INSERT INTO ventas (cliente, total, usuario_id) VALUES (%s, %s, %s)",
                (cliente, total, usuario_id),
            )
        )

    def agregar_detalle(self, venta_id: int, producto_id: int, cantidad: int, precio_unitario: float) -> int:
        subtotal = cantidad * precio_unitario
        return int(
            self.db.execute(
                """
                INSERT INTO detalles_venta (venta_id, producto_id, cantidad, precio_unitario, subtotal)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (venta_id, producto_id, cantidad, precio_unitario, subtotal),
            )
        )


