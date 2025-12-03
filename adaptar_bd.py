#!/usr/bin/env python3
"""
Script para adaptar la base de datos MySQL a la estructura que espera la aplicación
"""

import mysql.connector
from mysql.connector import Error
import json

def adaptar_base_datos():
    """Adaptar la base de datos a la estructura que espera la aplicación"""
    
    # Leer configuración
    with open('config_mysql.json', 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()
        
        print("=== ADAPTANDO BASE DE DATOS ===")
        
        # 1. Crear tabla de categorías si no existe
        print("1. Creando tabla de categorías...")
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS categorias (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(50) NOT NULL UNIQUE,
                descripcion TEXT,
                activo TINYINT(1) DEFAULT 1
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        ''')
        
        # 2. Insertar categorías por defecto
        print("2. Insertando categorías por defecto...")
        categorias = [
            ('Café', 'Cafés de diferentes tipos y preparaciones'),
            ('Té', 'Tés de diferentes sabores y tipos'),
            ('Bebidas Frías', 'Bebidas frías y refrescantes'),
            ('Postres', 'Postres y dulces'),
            ('Snacks', 'Snacks y botanas'),
            ('Desayunos', 'Productos de desayuno'),
            ('Sándwiches', 'Sándwiches y baguettes'),
            ('Otros', 'Otros productos')
        ]
        
        for categoria in categorias:
            cursor.execute("INSERT IGNORE INTO categorias (nombre, descripcion) VALUES (%s, %s)", categoria)
        
        # 3. Verificar si ya existe la columna categoria en productos
        cursor.execute("DESCRIBE productos")
        columnas = [columna[0] for columna in cursor.fetchall()]
        
        if 'categoria' not in columnas:
            print("3. Agregando columna 'categoria' a productos...")
            cursor.execute("ALTER TABLE productos ADD COLUMN categoria VARCHAR(50)")
            
            # Actualizar los productos existentes con categorías basadas en categoria_id
            cursor.execute("UPDATE productos SET categoria = 'Café' WHERE categoria_id = 1")
            cursor.execute("UPDATE productos SET categoria = 'Té' WHERE categoria_id = 2")
            cursor.execute("UPDATE productos SET categoria = 'Bebidas Frías' WHERE categoria_id = 3")
            cursor.execute("UPDATE productos SET categoria = 'Postres' WHERE categoria_id = 4")
            cursor.execute("UPDATE productos SET categoria = 'Snacks' WHERE categoria_id = 5")
            cursor.execute("UPDATE productos SET categoria = 'Desayunos' WHERE categoria_id = 6")
            cursor.execute("UPDATE productos SET categoria = 'Sándwiches' WHERE categoria_id = 7")
            cursor.execute("UPDATE productos SET categoria = 'Otros' WHERE categoria_id = 8")
            cursor.execute("UPDATE productos SET categoria = 'Café' WHERE categoria_id IS NULL OR categoria = ''")
        
        # 4. Verificar usuario admin con contraseña correcta
        print("4. Verificando usuario admin...")
        cursor.execute("SELECT id, username, password FROM usuarios WHERE username = 'admin'")
        admin = cursor.fetchone()
        
        if admin:
            print(f"  - Usuario admin encontrado (ID: {admin[0]})")
            # Verificar si la contraseña está en texto plano o hash
            if admin[2] == 'admin123':
                print("  - Contraseña en texto plano detectada, actualizando a hash...")
                import hashlib
                hashed_password = hashlib.sha256('admin123'.encode()).hexdigest()
                cursor.execute("UPDATE usuarios SET password = %s WHERE id = %s", (hashed_password, admin[0]))
            else:
                print("  - Contraseña ya está hasheada")
        else:
            print("  - Usuario admin no encontrado, creando uno...")
            import hashlib
            hashed_password = hashlib.sha256('admin123'.encode()).hexdigest()
            cursor.execute("""
                INSERT INTO usuarios (username, password, nombre, rol) 
                VALUES (%s, %s, %s, %s)
            """, ('admin', hashed_password, 'Administrador Principal', 'admin'))
        
        # 5. Asegurar que las configuraciones por defecto existan
        print("5. Verificando configuraciones por defecto...")
        configuraciones = [
            ('tema_actual', 'claro', 'Tema actual de la aplicación'),
            ('moneda', 'S/', 'Símbolo de moneda (Soles peruanos)'),
            ('stock_minimo_predeterminado', '10', 'Stock mínimo predeterminado'),
            ('cafeteria_nombre', 'Nexus Coffee', 'Nombre de la cafetería'),
            ('cafeteria_direccion', 'Av. Principal 123, Lima, Perú', 'Dirección de la cafetería'),
            ('cafeteria_telefono', '01-2345678', 'Teléfono de la cafetería'),
            ('cafeteria_email', 'info@nexuscoffee.com', 'Email de la cafetería'),
            ('cafeteria_ruc', '12345678901', 'RUC de la cafetería')
        ]
        
        for clave, valor, descripcion in configuraciones:
            cursor.execute("SELECT * FROM configuracion WHERE clave = %s", (clave,))
            if not cursor.fetchone():
                cursor.execute("INSERT INTO configuracion (clave, valor, descripcion) VALUES (%s, %s, %s)", 
                            (clave, valor, descripcion))
        
        # 6. Verificar algunos productos de ejemplo
        print("6. Verificando productos...")
        cursor.execute("SELECT COUNT(*) FROM productos")
        total_productos = cursor.fetchone()[0]
        print(f"  - Total de productos: {total_productos}")
        
        if total_productos == 0:
            print("  - No hay productos, agregando algunos de ejemplo...")
            productos_ejemplo = [
                ('Café Americano', 'Café', 8.50, 100, 10, 'Café negro tradicional'),
                ('Café Latte', 'Café', 12.00, 80, 10, 'Café con leche espumosa'),
                ('Té Verde', 'Té', 6.00, 50, 5, 'Té verde caliente'),
                ('Muffin de Arándanos', 'Postres', 5.50, 30, 5, 'Muffin esponjoso con arándanos'),
                ('Sándwich de Pollo', 'Sándwiches', 15.00, 25, 3, 'Sándwich caliente de pollo')
            ]
            
            for nombre, categoria, precio, stock, stock_minimo, descripcion in productos_ejemplo:
                cursor.execute("""
                    INSERT INTO productos (nombre, categoria, precio, stock, stock_minimo, descripcion)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (nombre, categoria, precio, stock, stock_minimo, descripcion))
        
        # 7. Verificar clientes
        print("7. Verificando clientes...")
        cursor.execute("SELECT COUNT(*) FROM clientes")
        total_clientes = cursor.fetchone()[0]
        print(f"  - Total de clientes: {total_clientes}")
        
        if total_clientes == 0:
            print("  - No hay clientes, agregando algunos de ejemplo...")
            clientes_ejemplo = [
                ('Cliente General', 'general@cliente.com', '000000000'),
                ('Juan Pérez', 'juan@email.com', '987654321'),
                ('María García', 'maria@email.com', '912345678')
            ]
            
            for nombre, email, telefono in clientes_ejemplo:
                cursor.execute("INSERT INTO clientes (nombre, email, telefono) VALUES (%s, %s, %s)",
                            (nombre, email, telefono))
        
        conn.commit()
        print("\n✓ Base de datos adaptada exitosamente!")
        print("\nResumen de cambios:")
        print("- Tabla de categorías creada")
        print("- Columna 'categoria' agregada a productos")
        print("- Usuario admin verificado/contraseña actualizada")
        print("- Configuraciones por defecto agregadas")
        print("- Productos y clientes de ejemplo verificados")
        
        cursor.close()
        conn.close()
        
    except Error as e:
        print(f"Error: {e}")
        if conn:
            conn.rollback()
            conn.close()

if __name__ == "__main__":
    adaptar_base_datos()