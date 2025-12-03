#!/usr/bin/env python3
import mysql.connector
import hashlib
import json

# Cargar configuración
with open('config_mysql.json', 'r') as f:
    config = json.load(f)

conn = mysql.connector.connect(
    host=config['host'],
    user=config['user'],
    password=config['password'],
    database=config['database'],
    port=config.get('port', 3306)
)
cursor = conn.cursor()

cursor.execute('SELECT username, password FROM usuarios WHERE username = "admin"')
result = cursor.fetchone()

if result:
    print('Usuario:', result[0])
    print('Hash actual:', result[1])
    print('Hash esperado:', hashlib.sha256('admin123'.encode()).hexdigest())
    print('¿Coinciden?', result[1] == hashlib.sha256('admin123'.encode()).hexdigest())
else:
    print('Usuario admin no encontrado')

conn.close()