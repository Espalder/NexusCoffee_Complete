#!/usr/bin/env python3
import hashlib
from typing import Optional

from models.usuario import Usuario
from nexus_core.db import MySQLDatabase


class AuthService:
    def __init__(self, db: MySQLDatabase):
        self.db = db

    def validar_login(self, username: str, password: str) -> Optional[Usuario]:
        if not username or not password:
            return None
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        users = self.db.execute(
            "SELECT * FROM usuarios WHERE username = %s AND password = %s",
            (username, password_hash),
        )
        if users:
            return Usuario.from_row(users[0])
        return None


