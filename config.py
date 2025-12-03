#!/usr/bin/env python3
"""
Archivo de configuración para Nexus Café
Contiene todas las configuraciones y constantes de la aplicación
"""

import os

# Configuración de la aplicación
APP_NAME = "Nexus Coffee"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "Sistema de Gestión Integral para Cafeterías"
DEVELOPER = "Nexus Coffee Development Team"

# Rutas de archivos
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "nexus_coffee.db")
PDFS_DIR = os.path.join(BASE_DIR, "pdfs_generados")
BACKUP_DIR = os.path.join(BASE_DIR, "backups")

# Configuración de la base de datos
DB_CONFIG = {
    "path": DB_PATH,
    "check_same_thread": False,
    "timeout": 20
}

# Configuración de temas
THEMES = {
    "claro": {
        "bg_color": "#ECF0F1",
        "fg_color": "#2C3E50",
        "accent_color": "#3498DB",
        "secondary_color": "#E67E22",
        "success_color": "#27AE60",
        "danger_color": "#E74C3C",
        "warning_color": "#F39C12",
        "card_bg": "white",
        "text_color": "#2C3E50"
    },
    "oscuro": {
        "bg_color": "#2C3E50",
        "fg_color": "#ECF0F1",
        "accent_color": "#3498DB",
        "secondary_color": "#E67E22",
        "success_color": "#27AE60",
        "danger_color": "#E74C3C",
        "warning_color": "#F39C12",
        "card_bg": "#34495E",
        "text_color": "#ECF0F1"
    }
}

# Configuración de ventana
WINDOW_CONFIG = {
    "title": f"{APP_NAME} - {APP_DESCRIPTION}",
    "width": 1200,
    "height": 800,
    "min_width": 800,
    "min_height": 600,
    "resizable": True,
    "icon": None  # Ruta al ícono de la aplicación
}

# Configuración de productos
PRODUCT_CONFIG = {
    "default_stock_minimo": 10,
    "max_stock": 1000,
    "min_price": 0.01,
    "max_price": 10000.0,
    "categories": [
        "Bebidas Calientes",
        "Bebidas Frías", 
        "Bebidas Especiales",
        "Panadería",
        "Comida",
        "Postres"
    ]
}

# Configuración de ventas
SALE_CONFIG = {
    "default_tax": 0.16,  # 16% de IVA
    "max_discount": 0.50,  # Máximo 50% de descuento
    "receipt_template": "default"
}

# Configuración de reportes
REPORT_CONFIG = {
    "pdf_author": APP_NAME,
    "pdf_subject": "Reportes de Gestión",
    "pdf_creator": APP_NAME,
    "company_name": APP_NAME,
    "company_address": "Cafetería Nexus",
    "company_phone": "Teléfono de contacto",
    "company_email": "contacto@nexus-coffee.com"
}

# Configuración de gráficos
CHART_CONFIG = {
    "default_figsize": (10, 6),
    "dpi": 100,
    "style": "seaborn-v0_8",
    "color_palette": [
        "#3498DB", "#E67E22", "#27AE60", 
        "#E74C3C", "#9B59B6", "#F39C12",
        "#1ABC9C", "#34495E", "#95A5A6"
    ],
    "background_color": "white",
    "grid": True
}

# Configuración de notificaciones
NOTIFICATION_CONFIG = {
    "stock_low_threshold": 0.2,  # 20% del stock mínimo
    "check_interval": 3600,  # Verificar cada hora
    "sound_enabled": False,
    "popup_enabled": True
}

# Configuración de respaldo
BACKUP_CONFIG = {
    "auto_backup": True,
    "backup_interval": 86400,  # Cada 24 horas
    "max_backups": 10,
    "compression": False,
    "encryption": False
}

# Configuración de usuarios
USER_CONFIG = {
    "default_role": "user",
    "roles": ["admin", "manager", "cashier", "user"],
    "password_min_length": 6,
    "session_timeout": 3600,  # 1 hora
    "max_failed_attempts": 3
}

# Configuración de logs
LOG_CONFIG = {
    "level": "INFO",
    "file": os.path.join(BASE_DIR, "nexus_coffee.log"),
    "max_size": 1048576,  # 1MB
    "backup_count": 5,
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
}

# Mensajes del sistema
MESSAGES = {
    "login_success": "Bienvenido a Nexus Coffee",
    "login_failed": "Usuario o contraseña incorrectos",
    "logout_success": "Sesión cerrada correctamente",
    "product_added": "Producto agregado correctamente",
    "product_updated": "Producto actualizado correctamente",
    "product_deleted": "Producto eliminado correctamente",
    "sale_completed": "Venta realizada correctamente",
    "backup_created": "Respaldo creado correctamente",
    "report_generated": "Reporte generado correctamente",
    "stock_low_warning": "Stock bajo detectado",
    "database_error": "Error en la base de datos",
    "validation_error": "Datos inválidos",
    "permission_error": "Sin permisos suficientes"
}

# Rutas de recursos
RESOURCES = {
    "images": os.path.join(BASE_DIR, "resources", "images"),
    "icons": os.path.join(BASE_DIR, "resources", "icons"),
    "templates": os.path.join(BASE_DIR, "resources", "templates"),
    "sounds": os.path.join(BASE_DIR, "resources", "sounds")
}

# Crear directorios necesarios si no existen
for dir_path in [PDFS_DIR, BACKUP_DIR]:
    if not os.path.exists(dir_path):
        try:
            os.makedirs(dir_path)
        except OSError:
            pass

# Validación de configuración
def validate_config():
    """Validar la configuración de la aplicación"""
    errors = []
    
    # Validar rutas
    if not os.path.isdir(BASE_DIR):
        errors.append(f"Directorio base no existe: {BASE_DIR}")
    
    # Validar configuraciones numéricas
    if PRODUCT_CONFIG["default_stock_minimo"] < 0:
        errors.append("Stock mínimo no puede ser negativo")
    
    if SALE_CONFIG["default_tax"] < 0 or SALE_CONFIG["default_tax"] > 1:
        errors.append("Impuesto debe estar entre 0 y 1")
    
    if WINDOW_CONFIG["width"] < 400 or WINDOW_CONFIG["height"] < 300:
        errors.append("Tamaño de ventana demasiado pequeño")
    
    return errors

# Ejecutar validación al importar
if __name__ != "__main__":
    config_errors = validate_config()
    if config_errors:
        print("⚠️  Advertencias de configuración:")
        for error in config_errors:
            print(f"  - {error}")

# Función auxiliar para obtener configuración
def get_config(section=None, key=None):
    """Obtener configuración específica"""
    if section is None:
        return globals()
    
    config_dict = globals().get(section.upper() + "_CONFIG")
    if config_dict and key:
        return config_dict.get(key)
    
    return config_dict

# Función auxiliar para obtener tema actual
def get_theme_colors(theme_name="claro"):
    """Obtener colores del tema especificado"""
    return THEMES.get(theme_name, THEMES["claro"])

# Exportar configuraciones importantes
__all__ = [
    'APP_NAME', 'APP_VERSION', 'DB_PATH', 'THEMES', 
    'WINDOW_CONFIG', 'PRODUCT_CONFIG', 'SALE_CONFIG',
    'REPORT_CONFIG', 'CHART_CONFIG', 'NOTIFICATION_CONFIG',
    'BACKUP_CONFIG', 'USER_CONFIG', 'LOG_CONFIG',
    'MESSAGES', 'RESOURCES', 'get_config', 'get_theme_colors'
]