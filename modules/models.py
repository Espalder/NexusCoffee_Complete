#!/usr/bin/env python3
"""
Módulo de modelos de datos para Nexus Café
"""

import hashlib

class Usuario:
    def __init__(self, db_manager):
        self.db_manager = db_manager
    
    def autenticar(self, username, password):
        """Autenticar un usuario por username y password"""
        try:
            # Hash de la contraseña
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            
            query = "SELECT * FROM usuarios WHERE username = %s AND password = %s"
            users = self.db_manager.ejecutar_query(query, (username, password_hash))
            
            if users:
                user = users[0]
                return {
                    'id': user[0],
                    'username': user[1],
                    'nombre': user[3],
                    'rol': user[4]
                }
            return None
            
        except Exception as e:
            print(f"Error autenticando usuario: {e}")
            return None

class Producto:
    def __init__(self, db_manager):
        self.db_manager = db_manager
    
    def obtener_todos(self):
        """Obtener todos los productos"""
        try:
            query = "SELECT id, nombre, categoria, precio, stock, stock_minimo FROM productos ORDER BY nombre"
            return self.db_manager.ejecutar_query(query)
        except Exception as e:
            print(f"Error obteniendo productos: {e}")
            return []
    
    def obtener_stock_bajo(self):
        """Obtener productos con stock bajo"""
        try:
            query = "SELECT id, nombre, categoria, precio, stock, stock_minimo FROM productos WHERE stock <= stock_minimo ORDER BY nombre"
            return self.db_manager.ejecutar_query(query)
        except Exception as e:
            print(f"Error obteniendo productos con stock bajo: {e}")
            return []

class Venta:
    def __init__(self, db_manager):
        self.db_manager = db_manager
    
    def obtener_todas(self):
        """Obtener todas las ventas"""
        try:
            query = "SELECT id, cliente, total, fecha FROM ventas ORDER BY fecha DESC"
            return self.db_manager.ejecutar_query(query)
        except Exception as e:
            print(f"Error obteniendo ventas: {e}")
            return []
    
    def obtener_ventas_por_periodo(self, fecha_inicio, fecha_fin):
        """Obtener ventas en un período de tiempo"""
        try:
            query = "SELECT id, cliente, total, fecha FROM ventas WHERE DATE(fecha) BETWEEN %s AND %s ORDER BY fecha"
            return self.db_manager.ejecutar_query(query, (fecha_inicio, fecha_fin))
        except Exception as e:
            print(f"Error obteniendo ventas por período: {e}")
            return []
    
    def obtener_total_ventas_por_dia(self, dias):
        """Obtener el total de ventas por día para los últimos N días"""
        try:
            query = """
                SELECT DATE(fecha) as dia, SUM(total) as total
                FROM ventas
                WHERE fecha >= DATE_SUB(CURRENT_DATE(), INTERVAL %s DAY)
                GROUP BY DATE(fecha)
                ORDER BY dia
            """
            return self.db_manager.ejecutar_query(query, (dias,))
        except Exception as e:
            print(f"Error obteniendo total de ventas por día: {e}")
            return []
    
    def obtener_productos_mas_vendidos(self, limite=5):
        """Obtener los productos más vendidos"""
        try:
            query = """
                SELECT p.nombre, SUM(dv.cantidad) as cantidad, SUM(dv.subtotal) as total
                FROM detalles_venta dv
                JOIN productos p ON dv.producto_id = p.id
                GROUP BY p.id, p.nombre
                ORDER BY cantidad DESC
                LIMIT %s
            """
            return self.db_manager.ejecutar_query(query, (limite,))
        except Exception as e:
            print(f"Error obteniendo productos más vendidos: {e}")
            return []

class Cliente:
    def __init__(self, db_manager):
        self.db_manager = db_manager
    
    def obtener_todos(self):
        """Obtener todos los clientes"""
        try:
            query = "SELECT id, nombre, email, telefono FROM clientes ORDER BY nombre"
            return self.db_manager.ejecutar_query(query)
        except Exception as e:
            print(f"Error obteniendo clientes: {e}")
            return []

    def obtener_clientes_frecuentes(self, limite=10, desde=None, hasta=None):
        """Obtener clientes frecuentes por número de compras en un periodo opcional"""
        try:
            base_query = """
                SELECT COALESCE(c.id, 0) AS id,
                       v.cliente AS nombre,
                       c.email,
                       c.telefono,
                       COUNT(v.id) AS compras,
                       SUM(v.total) AS total_gastado
                FROM ventas v
                LEFT JOIN clientes c ON c.nombre = v.cliente
                {filtro_fecha}
                GROUP BY v.cliente, c.id, c.email, c.telefono
                ORDER BY compras DESC, total_gastado DESC
                LIMIT %s
            """
            filtro_fecha = ""
            params = []
            if desde and hasta:
                filtro_fecha = "WHERE DATE(v.fecha) BETWEEN %s AND %s"
                params = [desde, hasta]
            elif desde:
                filtro_fecha = "WHERE DATE(v.fecha) >= %s"
                params = [desde]
            elif hasta:
                filtro_fecha = "WHERE DATE(v.fecha) <= %s"
                params = [hasta]
            query = base_query.format(filtro_fecha=filtro_fecha)
            return self.db_manager.ejecutar_query(query, tuple(params + [limite]))
        except Exception as e:
            print(f"Error obteniendo clientes frecuentes: {e}")
            return []

class Configuracion:
    def __init__(self, db_manager):
        self.db_manager = db_manager
    
    def obtener_configuracion(self):
        """Obtener toda la configuración"""
        try:
            query = "SELECT clave, valor FROM configuracion"
            resultados = self.db_manager.ejecutar_query(query)
            
            config = {}
            for clave, valor in resultados:
                config[clave] = valor
                
            return config
        except Exception as e:
            print(f"Error obteniendo configuración: {e}")
            return {}