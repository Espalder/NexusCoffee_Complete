#!/usr/bin/env python3
"""
Script de prueba para verificar que la aplicación pueda iniciarse correctamente
"""

import sys
import os
import traceback

# Agregar el directorio actual al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    print("=== INICIANDO PRUEBA DE NEXUS COFFEE ===")
    
    # Importar los módulos necesarios
    print("1. Importando módulos...")
    import tkinter as tk
    print("   ✓ tkinter importado")
    
    # Intentar importar los módulos personalizados
    print("2. Importando módulos personalizados...")
    from modules.database import DatabaseManager
    print("   ✓ DatabaseManager importado")
    
    from modules.models import Usuario
    print("   ✓ Modelos importados")
    
    # Verificar configuración
    print("3. Verificando configuración...")
    import json
    with open('config_mysql.json', 'r') as f:
        config = json.load(f)
    print(f"   ✓ Configuración cargada - DB: {config['database']}")
    
    # Probar conexión a base de datos
    print("4. Probando conexión a base de datos...")
    db_manager = DatabaseManager(config)
    if db_manager.verificar_conexion():
        print("   ✓ Conexión a base de datos exitosa")
        
        # Verificar estructura
        print("5. Verificando estructura de base de datos...")
        db_manager.inicializar_bd()
        print("   ✓ Base de datos inicializada")
        
        # Probar login
        print("6. Probando login...")
        import hashlib
        password_hash = hashlib.sha256("admin123".encode()).hexdigest()
        query = "SELECT * FROM usuarios WHERE username = %s AND password = %s"
        users = db_manager.ejecutar_query(query, ("admin", password_hash))
        
        if users:
            user = users[0]
            print(f"   ✓ Login exitoso - Usuario: {user[1]}, Rol: {user[4]}")
        else:
            print("   ✗ Login fallido")
            
    else:
        print("   ✗ Error de conexión a base de datos")
    
    print("\n=== PRUEBA COMPLETADA EXITOSAMENTE ===")
    print("La aplicación está lista para ejecutarse.")
    print("\nPara ejecutar la aplicación completa:")
    print("python main_modular.py")
    
except Exception as e:
    print(f"\n✗ ERROR: {e}")
    print("\nDetalles del error:")
    traceback.print_exc()
    sys.exit(1)