#!/usr/bin/env python3
"""
Script para verificar la estructura exacta de las tablas MySQL
"""

import mysql.connector
from mysql.connector import Error
import json

def verificar_estructura_completa():
    """Verificar la estructura completa de todas las tablas"""
    
    # Leer configuración
    with open('config_mysql.json', 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()
        
        # Verificar estructura de cada tabla
        tablas = ['usuarios', 'productos', 'ventas', 'detalles_venta', 'clientes', 'configuracion']
        
        for tabla in tablas:
            print(f"\n=== ESTRUCTURA DE TABLA '{tabla}' ===")
            cursor.execute(f"DESCRIBE {tabla}")
            columnas = cursor.fetchall()
            
            print(f"Columnas de {tabla}:")
            for columna in columnas:
                print(f"  - {columna[0]}: {columna[1]} {columna[2]} {columna[3]}")
        
        # Verificar índices
        print(f"\n=== ÍNDICES DE TABLA 'productos' ===")
        cursor.execute("SHOW INDEX FROM productos")
        indices = cursor.fetchall()
        for indice in indices:
            print(f"  - {indice[2]}: {indice[4]} ({indice[3]})")
        
        cursor.close()
        conn.close()
        
    except Error as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    verificar_estructura_completa()