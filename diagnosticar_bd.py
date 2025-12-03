#!/usr/bin/env python3
"""
Script de diagnóstico para verificar la conexión y estructura de la base de datos Nexus Coffee
"""

import mysql.connector
import json
import hashlib
from datetime import datetime

def cargar_config():
    """Cargar configuración de la base de datos"""
    try:
        with open('config_mysql.json', 'r') as f:
            config = json.load(f)
        return config
    except FileNotFoundError:
        print("No se encontró config_mysql.json, usando configuración por defecto")
        return {
            'host': 'localhost',
            'user': 'root',
            'password': '',
            'database': 'nexus_coffee',
            'port': 3306
        }

def conectar_bd(config):
    """Conectar a la base de datos"""
    try:
        conn = mysql.connector.connect(
            host=config['host'],
            user=config['user'],
            password=config['password'],
            database=config['database'],
            port=config.get('port', 3306)
        )
        return conn
    except mysql.connector.Error as e:
        print(f"Error conectando a la base de datos: {e}")
        return None

def verificar_configuracion():
    """Verificar la configuración"""
    print("=== VERIFICACIÓN DE CONFIGURACIÓN ===")
    config = cargar_config()
    print(f"✓ Configuración encontrada:")
    print(f"  - Host: {config['host']}")
    print(f"  - Usuario: {config['user']}")
    print(f"  - Base de datos: {config['database']}")
    print(f"  - Puerto: {config.get('port', 3306)}")
    return config

def verificar_conexion_mysql(config):
    """Verificar la conexión a MySQL"""
    print("\n=== VERIFICACIÓN DE CONEXIÓN MYSQL ===")
    conn = conectar_bd(config)
    if conn:
        print("✓ Conexión a MySQL exitosa")
        cursor = conn.cursor()
        cursor.execute("SELECT DATABASE()")
        db_name = cursor.fetchone()[0]
        print(f"✓ Base de datos '{db_name}' seleccionada")
        conn.close()
        return True
    else:
        print("✗ Error conectando a MySQL")
        return False

def verificar_estructura_bd(config):
    """Verificar la estructura de la base de datos"""
    print("\n=== VERIFICACIÓN DE ESTRUCTURA DE 'nexus_coffee' ===")
    conn = conectar_bd(config)
    if not conn:
        return
    
    cursor = conn.cursor()
    
    # Verificar tablas
    cursor.execute("SHOW TABLES")
    tablas = cursor.fetchall()
    
    print(f"✓ Tablas encontradas ({len(tablas)}):")
    
    # Verificar cada tabla
    tablas_principales = ['usuarios', 'productos', 'ventas', 'detalles_venta', 'clientes', 'configuracion']
    
    for tabla in tablas_principales:
        try:
            # Contar registros
            cursor.execute(f"SELECT COUNT(*) FROM {tabla}")
            count = cursor.fetchone()[0]
            
            # Verificar columnas
            cursor.execute(f"DESCRIBE {tabla}")
            columnas = cursor.fetchall()
            
            print(f"  ✓ {tabla}")
            print(f"    - Registros: {count}")
            print(f"    - Columnas: {len(columnas)}")
            
        except mysql.connector.Error as e:
            print(f"  ✗ Error en {tabla}: {e}")
    
    conn.close()

def mostrar_muestra_datos(config):
    """Mostrar una muestra de los datos"""
    print("\n=== MUESTRA DE DATOS ===")
    conn = conectar_bd(config)
    if not conn:
        return
    
    cursor = conn.cursor()
    
    # Usuarios
    print("Usuarios encontrados:")
    cursor.execute("SELECT id, username, nombre, rol FROM usuarios LIMIT 3")
    usuarios = cursor.fetchall()
    for usuario in usuarios:
        print(f"  - ID: {usuario[0]}, Username: {usuario[1]}, Nombre: {usuario[2]}, Rol: {usuario[3]}")
    
    # Productos
    print("Productos encontrados:")
    cursor.execute("SELECT id, nombre, categoria, precio, stock FROM productos LIMIT 3")
    productos = cursor.fetchall()
    for producto in productos:
        print(f"  - ID: {producto[0]}, Nombre: {producto[1]}, Categoría: {producto[2]}, Precio: {producto[3]}, Stock: {producto[4]}")
    
    # Configuración
    print("Configuración encontrada:")
    cursor.execute("SELECT clave, valor FROM configuracion LIMIT 5")
    config_items = cursor.fetchall()
    for clave, valor in config_items:
        print(f"  - {clave}: {valor}")
    
    conn.close()

def probar_queries_comunes(config):
    """Probar queries comunes que usa la aplicación"""
    print("\n=== PRUEBA DE QUERIES COMUNES ===")
    conn = conectar_bd(config)
    if not conn:
        return
    
    cursor = conn.cursor()
    
    # Query de login
    print("1. Query de login:")
    password_hash = hashlib.sha256("admin123".encode()).hexdigest()
    cursor.execute("SELECT * FROM usuarios WHERE username = %s AND password = %s", ("admin", password_hash))
    login_result = cursor.fetchone()
    if login_result:
        print("  ✓ Login exitoso")
        print(f"    - Usuario: {login_result[1]}")
        print(f"    - Nombre: {login_result[3]}")
        print(f"    - Rol: {login_result[4]}")
    else:
        print("  ✗ Login fallido - credenciales admin/admin123 no encontradas")
    
    # Query de productos
    print("\n2. Query de productos:")
    try:
        cursor.execute("SELECT id, nombre, categoria, precio, stock, stock_minimo FROM productos ORDER BY nombre LIMIT 5")
        productos = cursor.fetchall()
        print(f"  ✓ Query de productos funciona ({len(productos)} productos)")
        for prod in productos[:3]:
            print(f"    - {prod[1]}: {prod[2]} - S/{prod[3]} (Stock: {prod[4]})")
    except mysql.connector.Error as e:
        print(f"  ✗ Error en query de productos: {e}")
    
    # Query de ventas
    print("\n3. Query de ventas:")
    try:
        cursor.execute("SELECT id, cliente, total, fecha FROM ventas ORDER BY fecha DESC LIMIT 5")
        ventas = cursor.fetchall()
        print(f"  ✓ Query de ventas funciona ({len(ventas)} ventas)")
        for venta in ventas[:3]:
            print(f"    - Venta #{venta[0]}: {venta[1]} - S/{venta[2]} - {venta[3]}")
    except mysql.connector.Error as e:
        print(f"  ✗ Error en query de ventas: {e}")
    
    # Query de clientes
    print("\n4. Query de clientes:")
    try:
        cursor.execute("SELECT id, nombre, email, telefono FROM clientes ORDER BY nombre LIMIT 5")
        clientes = cursor.fetchall()
        print(f"  ✓ Query de clientes funciona ({len(clientes)} clientes)")
        for cliente in clientes[:3]:
            print(f"    - {cliente[1]}: {cliente[2]} - {cliente[3]}")
    except mysql.connector.Error as e:
        print(f"  ✗ Error en query de clientes: {e}")
    
    conn.close()

def main():
    """Función principal de diagnóstico"""
    print("DIAGNÓSTICO DE BASE DE DATOS NEXUS COFFEE")
    print("=" * 50)
    print(f"Fecha y hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Verificar configuración
    config = verificar_configuracion()
    
    # Verificar conexión
    if verificar_conexion_mysql(config):
        # Verificar estructura
        verificar_estructura_bd(config)
        
        # Mostrar datos de muestra
        mostrar_muestra_datos(config)
        
        # Probar queries
        probar_queries_comunes(config)
        
        print("\n" + "=" * 50)
        print("Diagnóstico completado")
        print("=" * 50)
    else:
        print("No se pudo continuar con el diagnóstico debido a problemas de conexión")

if __name__ == "__main__":
    main()