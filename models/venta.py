#!/usr/bin/env python3
from dataclasses import dataclass
from typing import Optional, List, Tuple
from datetime import datetime


@dataclass
class Venta:
    id: Optional[int]
    cliente: str
    total: float
    fecha: Optional[datetime]
    usuario_nombre: Optional[str]

    @staticmethod
    def from_row(row: Tuple) -> "Venta":
        # row = (id, cliente, total, fecha, usuario_nombre)
        return Venta(
            id=row[0],
            cliente=row[1],
            total=float(row[2]) if row[2] is not None else 0.0,
            fecha=row[3],
            usuario_nombre=row[4] if len(row) > 4 else None,
        )


