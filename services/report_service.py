#!/usr/bin/env python3
from typing import List, Tuple
from nexus_core.db import MySQLDatabase


class ReportService:
    def __init__(self, db: MySQLDatabase):
        self.db = db

    def ventas_por_dia(self) -> List[Tuple[str, float]]:
        rows = self.db.execute(
            """
            SELECT DATE(fecha) as dia, SUM(total) as total_ventas
            FROM ventas
            WHERE fecha >= DATE_SUB(CURDATE(), INTERVAL 7 DAY)
            GROUP BY DATE(fecha)
            ORDER BY dia
            """
        )
        return rows or []

    def ventas_por_producto(self) -> List[Tuple[str, int]]:
        rows = self.db.execute(
            """
            SELECT p.nombre, SUM(dv.cantidad) as total_vendido
            FROM detalles_venta dv
            JOIN productos p ON dv.producto_id = p.id
            JOIN ventas v ON dv.venta_id = v.id
            WHERE v.fecha >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
            GROUP BY p.id
            ORDER BY total_vendido DESC
            LIMIT 10
            """
        )
        return rows or []

    def productos_por_categoria(self) -> List[Tuple[str, int]]:
        rows = self.db.execute(
            """
            SELECT categoria, COUNT(*) as total
            FROM productos
            GROUP BY categoria
            ORDER BY total DESC
            """
        )
        return rows or []


