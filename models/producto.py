#!/usr/bin/env python3
from dataclasses import dataclass
from typing import Optional, Tuple


@dataclass
class Producto:
    id: Optional[int]
    nombre: str
    categoria: str
    precio: float
    stock: int
    stock_minimo: int
    descripcion: Optional[str] = None

    @staticmethod
    def from_row(row: Tuple) -> "Producto":
        # row = (id, nombre, categoria, precio, stock, stock_minimo, descripcion, ...)
        return Producto(
            id=row[0],
            nombre=row[1],
            categoria=row[2],
            precio=float(row[3]),
            stock=int(row[4]),
            stock_minimo=int(row[5]),
            descripcion=row[6] if len(row) > 6 else None,
        )


