#!/usr/bin/env python3
"""
Script para actualizar la estructura de la base de datos de nexus_coffee
para que sea compatible con la aplicación
"""

import mysql.connector
from mysql.connector import Error
import json
import os

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
    except Error as e:
        print(f"Error conectando a la base de datos: {e}")
        return None

def actualizar_estructura_ventas(cursor):
    """Actualizar la estructura de la tabla ventas"""
    print("=== ACTUALIZANDO ESTRUCTURA DE VENTAS ===")
    
    # Verificar si existe la columna cliente
    cursor.execute("""
        SELECT COLUMN_NAME 
        FROM INFORMATION_SCHEMA.COLUMNS 
        WHERE TABLE_SCHEMA = DATABASE() 
        AND TABLE_NAME = 'ventas' 
        AND COLUMN_NAME = 'cliente'
    """)
    tiene_cliente = cursor.fetchone() is not None
    
    # Verificar si existe la columna cliente_id
    cursor.execute("""
        SELECT COLUMN_NAME 
        FROM INFORMATION_SCHEMA.COLUMNS 
        WHERE TABLE_SCHEMA = DATABASE() 
        AND TABLE_NAME = 'ventas' 
        AND COLUMN_NAME = 'cliente_id'
    """)
    tiene_cliente_id = cursor.fetchone() is not None
    
    if tiene_cliente_id and not tiene_cliente:
        print("- Agregando columna cliente a ventas...")
        cursor.execute("ALTER TABLE ventas ADD COLUMN cliente VARCHAR(255) NULL")
        
        # Actualizar los valores de cliente basados en cliente_id
        print("- Actualizando valores de cliente...")
        cursor.execute("""
            UPDATE ventas v 
            LEFT JOIN clientes c ON v.cliente_id = c.id 
            SET v.cliente = COALESCE(c.nombre, 'Cliente General')
        """)
        
        print("- Eliminando columna cliente_id...")
        cursor.execute("ALTER TABLE ventas DROP FOREIGN KEY ventas_ibfk_1")
        cursor.execute("ALTER TABLE ventas DROP COLUMN cliente_id")
        
        print("- Agregando índice a cliente...")
        cursor.execute("ALTER TABLE ventas ADD INDEX idx_cliente (cliente)")
        
    elif tiene_cliente and tiene_cliente_id:
        print("- Ambas columnas existen, eliminando cliente_id...")
        cursor.execute("ALTER TABLE ventas DROP FOREIGN KEY ventas_ibfk_1")
        cursor.execute("ALTER TABLE ventas DROP COLUMN cliente_id")
        
    print("✓ Estructura de ventas actualizada")

def actualizar_triggers(cursor):
    """Actualizar triggers para usar cliente en lugar de cliente_id"""
    print("=== ACTUALIZANDO TRIGGERS ===")
    
    # Eliminar trigger existente
    try:
        cursor.execute("DROP TRIGGER IF EXISTS auditoria_ventas")
        print("- Trigger anterior eliminado")
    except:
        pass
    
    # Crear nuevo trigger con cliente
    cursor.execute("""
        CREATE TRIGGER auditoria_ventas
        AFTER INSERT ON ventas
        FOR EACH ROW
        BEGIN
            INSERT INTO auditoria (tabla, accion, descripcion, usuario_id, fecha)
            VALUES ('ventas', 'INSERT', 
                    CONCAT('Venta #', NEW.id, ' - Cliente: ', NEW.cliente, ' - Total: S/', NEW.total), 
                    NEW.usuario_id, NOW());
        END
    """)
    print("- Trigger actualizado con cliente")

def actualizar_configuraciones(cursor):
    """Actualizar configuraciones por defecto"""
    print("=== VERIFICANDO CONFIGURACIONES ===")
    
    configuraciones = [
        ('stock_minimo_default', '10'),
        ('tema_actual', 'claro'),
        ('iva_porcentaje', '16'),
        ('moneda', 'PEN'),
        ('nombre_cafeteria', 'Nexus Coffee')
    ]
    
    for clave, valor in configuraciones:
        cursor.execute("SELECT COUNT(*) FROM configuracion WHERE clave = %s", (clave,))
        if cursor.fetchone()[0] == 0:
            cursor.execute("INSERT INTO configuracion (clave, valor) VALUES (%s, %s)", (clave, valor))
            print(f"- Configuración agregada: {clave} = {valor}")
        else:
            print(f"- Configuración ya existe: {clave}")

def actualizar_admin_password(cursor):
    """Actualizar contraseña del admin con hash SHA256"""
    print("=== ACTUALIZANDO CONTRASEÑA ADMIN ===")
    
    import hashlib
    admin_password = hashlib.sha256("admin123".encode()).hexdigest()
    
    cursor.execute("UPDATE usuarios SET password = %s WHERE username = 'admin'", (admin_password,))
    print("- Contraseña admin actualizada con hash SHA256")

def main():
    """Función principal"""
    print("=== ACTUALIZANDO ESTRUCTURA DE BASE DE DATOS ===")
    
    config = cargar_config()
    conn = conectar_bd(config)
    
    if not conn:
        print("No se pudo conectar a la base de datos")
        return
    
    try:
        cursor = conn.cursor()
        
        # Actualizar estructura de ventas
        actualizar_estructura_ventas(cursor)
        
        # Actualizar triggers
        actualizar_triggers(cursor)
        
        # Actualizar configuraciones
        actualizar_configuraciones(cursor)
        
        # Actualizar contraseña admin
        actualizar_admin_password(cursor)
        
        # Confirmar cambios
        conn.commit()
        print("\n✓ Estructura de base de datos actualizada exitosamente!")
        
        # Verificar estructura final
        print("\n=== VERIFICACIÓN FINAL ===")
        cursor.execute("DESCRIBE ventas")
        columnas = cursor.fetchall()
        print("Columnas de ventas:")
        for col in columnas:
            print(f"  - {col[0]}: {col[1]}")
        
    except Error as e:
        print(f"Error actualizando estructura: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    main()