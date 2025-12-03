#!/usr/bin/env python3
from typing import List, Optional, Tuple

from models.producto import Producto
from nexus_core.db import MySQLDatabase


class ProductoService:
    def __init__(self, db: MySQLDatabase):
        self.db = db

    def listar(self) -> List[Producto]:
        rows = self.db.execute(
            "SELECT id, nombre, categoria, precio, stock, stock_minimo, descripcion FROM productos ORDER BY nombre"
        )
        return [Producto.from_row(r) for r in rows] if rows else []

    def buscar(self, texto: str) -> List[Producto]:
        rows = self.db.execute(
            """
            SELECT id, nombre, categoria, precio, stock, stock_minimo, descripcion
            FROM productos
            WHERE nombre LIKE %s OR categoria LIKE %s
            ORDER BY nombre
            """,
            (f"%{texto}%", f"%{texto}%"),
        )
        return [Producto.from_row(r) for r in rows] if rows else []

    def agregar(self, p: Producto) -> int:
        return int(
            self.db.execute(
                """
                INSERT INTO productos (nombre, categoria, precio, stock, stock_minimo, descripcion)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (p.nombre, p.categoria, p.precio, p.stock, p.stock_minimo, p.descripcion),
            )
        )

    def actualizar(self, p: Producto) -> int:
        return int(
            self.db.execute(
                """
                UPDATE productos
                SET nombre=%s, categoria=%s, precio=%s, stock=%s, stock_minimo=%s, descripcion=%s
                WHERE id=%s
                """,
                (p.nombre, p.categoria, p.precio, p.stock, p.stock_minimo, p.descripcion, p.id),
            )
        )

    def eliminar(self, producto_id: int) -> int:
        return int(self.db.execute("DELETE FROM productos WHERE id = %s", (producto_id,)))

    def stock_disponible(self, producto_id: int) -> Optional[int]:
        rows = self.db.execute("SELECT stock FROM productos WHERE id = %s", (producto_id,))
        return int(rows[0][0]) if rows else None


