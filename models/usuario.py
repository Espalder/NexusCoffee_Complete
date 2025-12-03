#!/usr/bin/env python3
from dataclasses import dataclass


@dataclass
class Usuario:
    id: int
    username: str
    nombre: str
    rol: str = "admin"

    @staticmethod
    def from_row(row: tuple) -> "Usuario":
        # row = (id, username, password, nombre, rol, fecha_creacion)
        return Usuario(id=row[0], username=row[1], nombre=row[3], rol=row[4])


