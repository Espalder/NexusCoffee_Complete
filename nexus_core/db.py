#!/usr/bin/env python3
"""
Módulo de acceso a datos MySQL centralizado
"""

import mysql.connector
from mysql.connector import Error
from typing import Any, Dict, Iterable, Optional, Tuple, Union, List


class MySQLDatabase:
    def __init__(self, config: Dict[str, Any]):
        self.config = config

    def check_connection(self) -> bool:
        try:
            conn = mysql.connector.connect(
                host=self.config['host'],
                user=self.config['user'],
                password=self.config['password'],
                port=self.config.get('port', 3306)
            )
            conn.close()
            return True
        except Error:
            return False

    def execute(self, query: str, params: Optional[Union[Tuple[Any, ...], List[Any]]] = None):
        conn = None
        cursor = None
        try:
            conn = mysql.connector.connect(**self.config)
            cursor = conn.cursor()

            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)

            upper = query.strip().upper()
            if upper.startswith("INSERT"):
                conn.commit()
                return cursor.lastrowid
            if upper.startswith("UPDATE") or upper.startswith("DELETE"):
                conn.commit()
                return cursor.rowcount
            return cursor.fetchall()
        except Error as e:
            if conn:
                conn.rollback()
            raise e
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()


