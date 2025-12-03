#!/usr/bin/env python3
"""Configuración centralizada de MySQL para Nexus Café"""

import os
import json
from typing import Dict, Any


DEFAULT_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'nexus_coffee',
    'port': 3306,
}


def get_mysql_config() -> Dict[str, Any]:
    # 1) Intentar leer de variables de entorno
    cfg = {
        'host': os.getenv('MYSQL_HOST', DEFAULT_CONFIG['host']),
        'user': os.getenv('MYSQL_USER', DEFAULT_CONFIG['user']),
        'password': os.getenv('MYSQL_PASSWORD', DEFAULT_CONFIG['password']),
        'database': os.getenv('MYSQL_DATABASE', DEFAULT_CONFIG['database']),
        'port': int(os.getenv('MYSQL_PORT', DEFAULT_CONFIG['port'])),
    }

    # 2) Intentar sobrescribir desde archivo local config_mysql.json si existe
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.abspath(os.path.join(base_dir, os.pardir))
        candidate_paths = [
            os.path.join(project_root, 'config_mysql.json'),
            os.path.join(project_root, 'configuracion.json'),
        ]
        for path in candidate_paths:
            if os.path.isfile(path):
                with open(path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for key in ['host', 'user', 'password', 'database', 'port']:
                        if key in data:
                            cfg[key] = data[key] if key != 'port' else int(data[key])
                break
    except Exception:
        pass

    return cfg


