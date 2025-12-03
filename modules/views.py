#!/usr/bin/env python3
"""
Módulo de vistas para Nexus Café
Contiene las clases para las diferentes vistas de la aplicación
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import pandas as pd
from datetime import datetime, timedelta
import os

class LoginView:
    def __init__(self, root, tema, on_login, cafeteria_info):
        self.root = root
        self.tema = tema
        self.on_login = on_login
        self.cafeteria_info = cafeteria_info
        self.mostrar()
        
    def mostrar(self):
        """Mostrar ventana de login"""
        # Frame principal
        frame_login = tk.Frame(self.root, bg="#34495E", padx=50, pady=50)
        frame_login.place(relx=0.5, rely=0.5, anchor="center")
        
        # Título
        titulo = tk.Label(frame_login, text="NEXUS CAFÉ", 
                         font=("Arial", 24, "bold"), fg="#E67E22", bg="#34495E")
        titulo.pack(pady=(0, 30))
        
        # Logo
        try:
            logo_frame = tk.Frame(frame_login, bg="#34495E", width=100, height=100)
            logo_frame.pack(pady=(0, 20))
            logo_label = tk.Label(logo_frame, text="☕", font=("Arial", 48), 
                                bg="#34495E", fg="#E67E22")
            logo_label.pack()
        except:
            pass
        
        # Campos de entrada
        tk.Label(frame_login, text="Usuario:", font=("Arial", 12), 
                bg="#34495E", fg="white").pack(anchor="w")
        self.entry_usuario = tk.Entry(frame_login, font=("Arial", 12), width=25)
        self.entry_usuario.pack(pady=(5, 15))
        
        tk.Label(frame_login, text="Contraseña:", font=("Arial", 12), 
                bg="#34495E", fg="white").pack(anchor="w")
        self.entry_password = tk.Entry(frame_login, font=("Arial", 12), 
                                     width=25, show="*")
        self.entry_password.pack(pady=(5, 20))
        
        # Botón de login
        btn_login = tk.Button(frame_login, text="Iniciar Sesión", 
                             command=self.validar_login,
                             bg="#E67E22", fg="white", font=("Arial", 12, "bold"),
                             width=20, cursor="hand2")
        btn_login.pack(pady=10)
        
        # Información
        info = tk.Label(frame_login, text="Usuario: admin | Contraseña: admin123", 
                       font=("Arial", 10), bg="#34495E", fg="#BDC3C7")
        info.pack(pady=(20, 0))
        
        # Bind Enter key
        self.root.bind('<Return>', lambda e: self.validar_login())
        
    def validar_login(self):
        """Validar credenciales de usuario"""
        usuario = self.entry_usuario.get()
        password = self.entry_password.get()
        
        if not usuario or not password:
            messagebox.showerror("Error", "Por favor complete todos los campos")
            return
        
        # Llamar al callback de login
        self.on_login(usuario, password)


class DashboardView:
    def __init__(self, root, tema, usuario, models, pdf_generator, on_logout, cafeteria_info):
        self.root = root
        self.tema = tema
        self.usuario = usuario
        self.models = models
        self.pdf_generator = pdf_generator
        self.on_logout = on_logout
        self.cafeteria_info = cafeteria_info
        self.mostrar()
        
    def mostrar(self):
        """Mostrar dashboard principal"""
        # Configurar ventana principal
        self.root.configure(bg="#ECF0F1")
        
        # Crear menú superior
        self.crear_menu_superior()
        
        # Frame principal
        frame_main = tk.Frame(self.root, bg="#ECF0F1")
        frame_main.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Título del dashboard
        titulo = tk.Label(frame_main, text=f"Bienvenido, {self.usuario['nombre']}", 
                         font=("Arial", 24, "bold"), bg="#ECF0F1", fg="#2C3E50")
        titulo.pack(pady=(0, 20), anchor="w")
        
        # Crear grid de 2x2 para widgets del dashboard
        frame_grid = tk.Frame(frame_main, bg="#ECF0F1")
        frame_grid.pack(fill=tk.BOTH, expand=True)
        
        # Configurar grid
        frame_grid.grid_columnconfigure(0, weight=1)
        frame_grid.grid_columnconfigure(1, weight=1)
        frame_grid.grid_rowconfigure(0, weight=1)
        frame_grid.grid_rowconfigure(1, weight=1)
        
        # Widget 1: Resumen de ventas
        self.crear_widget_resumen_ventas(frame_grid, 0, 0)
        
        # Widget 2: Productos con stock bajo
        self.crear_widget_stock_bajo(frame_grid, 0, 1)
        
        # Widget 3: Gráfico de ventas
        self.crear_widget_grafico_ventas(frame_grid, 1, 0)
        
        # Widget 4: Productos más vendidos
        self.crear_widget_productos_vendidos(frame_grid, 1, 1)
        
    def crear_menu_superior(self):
        """Crear menú superior"""
        menu_frame = tk.Frame(self.root, bg="#2C3E50", height=50)
        menu_frame.pack(fill=tk.X)
        
        # Logo
        logo_label = tk.Label(menu_frame, text="☕ NEXUS CAFÉ", 
                             font=("Arial", 14, "bold"), bg="#2C3E50", fg="#ECF0F1")
        logo_label.pack(side=tk.LEFT, padx=20)
        
        # Botones de navegación
        btn_dashboard = tk.Button(menu_frame, text="Dashboard", bg="#2C3E50", fg="#ECF0F1",
                                 font=("Arial", 10), bd=0, cursor="hand2")
        btn_dashboard.pack(side=tk.LEFT, padx=10)
        
        btn_ventas = tk.Button(menu_frame, text="Ventas", bg="#2C3E50", fg="#ECF0F1",
                              font=("Arial", 10), bd=0, cursor="hand2")
        btn_ventas.pack(side=tk.LEFT, padx=10)
        
        btn_inventario = tk.Button(menu_frame, text="Inventario", bg="#2C3E50", fg="#ECF0F1",
                                  font=("Arial", 10), bd=0, cursor="hand2")
        btn_inventario.pack(side=tk.LEFT, padx=10)
        
        btn_reportes = tk.Button(menu_frame, text="Reportes", bg="#2C3E50", fg="#ECF0F1",
                                font=("Arial", 10), bd=0, cursor="hand2")
        btn_reportes.pack(side=tk.LEFT, padx=10)
        
        btn_config = tk.Button(menu_frame, text="Configuración", bg="#2C3E50", fg="#ECF0F1",
                              font=("Arial", 10), bd=0, cursor="hand2")
        btn_config.pack(side=tk.LEFT, padx=10)
        
        # Información de usuario y botón de salir
        frame_usuario = tk.Frame(menu_frame, bg="#2C3E50")
        frame_usuario.pack(side=tk.RIGHT, padx=20)
        
        label_usuario = tk.Label(frame_usuario, text=f"Usuario: {self.usuario['username']}", 
                                bg="#2C3E50", fg="#ECF0F1", font=("Arial", 10))
        label_usuario.pack(side=tk.LEFT, padx=(0, 10))
        
        btn_salir = tk.Button(frame_usuario, text="Salir", bg="#E74C3C", fg="white",
                             font=("Arial", 10), cursor="hand2", command=self.on_logout)
        btn_salir.pack(side=tk.LEFT)
        
    def crear_widget_resumen_ventas(self, parent, row, col):
        """Crear widget de resumen de ventas"""
        frame = tk.Frame(parent, bg="white", bd=1, relief=tk.SOLID)
        frame.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
        
        # Título
        tk.Label(frame, text="Resumen de Ventas", font=("Arial", 14, "bold"), 
                bg="white", fg="#2C3E50").pack(pady=(15, 10), padx=15, anchor="w")
        
        # Contenido
        try:
            # Obtener datos
            hoy = datetime.now().strftime('%Y-%m-%d')
            ayer = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
            
            # Ventas de hoy
            ventas_hoy = self.models['venta'].obtener_ventas_por_periodo(f"{hoy} 00:00:00", f"{hoy} 23:59:59")
            total_hoy = sum(venta[2] for venta in ventas_hoy) if ventas_hoy else 0
            
            # Ventas de ayer
            ventas_ayer = self.models['venta'].obtener_ventas_por_periodo(f"{ayer} 00:00:00", f"{ayer} 23:59:59")
            total_ayer = sum(venta[2] for venta in ventas_ayer) if ventas_ayer else 0
            
            # Mostrar información
            frame_info = tk.Frame(frame, bg="white")
            frame_info.pack(fill=tk.X, padx=15, pady=10)
            
            # Ventas de hoy
            tk.Label(frame_info, text="Ventas de hoy:", font=("Arial", 12), 
                    bg="white", fg="#2C3E50").grid(row=0, column=0, sticky="w", pady=5)
            tk.Label(frame_info, text=f"S/ {total_hoy:.2f}", font=("Arial", 12, "bold"), 
                    bg="white", fg="#27AE60").grid(row=0, column=1, sticky="e", pady=5)
            
            # Ventas de ayer
            tk.Label(frame_info, text="Ventas de ayer:", font=("Arial", 12), 
                    bg="white", fg="#2C3E50").grid(row=1, column=0, sticky="w", pady=5)
            tk.Label(frame_info, text=f"S/ {total_ayer:.2f}", font=("Arial", 12, "bold"), 
                    bg="white", fg="#2980B9").grid(row=1, column=1, sticky="e", pady=5)
            
            # Comparación
            diferencia = total_hoy - total_ayer
            color = "#27AE60" if diferencia >= 0 else "#E74C3C"
            signo = "+" if diferencia >= 0 else ""

            porcentaje = "N/A"
            if total_ayer > 0:
                porcentaje = f"{signo}{diferencia/total_ayer*100:.1f}%"

            tk.Label(frame_info, text="Diferencia:", font=("Arial", 12), 
                    bg="white", fg="#2C3E50").grid(row=2, column=0, sticky="w", pady=5)
            tk.Label(frame_info, text=f"{signo}{diferencia:.2f} ({porcentaje})", 
                    font=("Arial", 12, "bold"), bg="white", fg=color).grid(row=2, column=1, sticky="e", pady=5)
            
        except Exception as e:
            tk.Label(frame, text=f"Error al cargar datos: {e}", 
                    bg="white", fg="#E74C3C").pack(pady=10, padx=15)
    
    def crear_widget_stock_bajo(self, parent, row, col):
        """Crear widget de productos con stock bajo"""
        frame = tk.Frame(parent, bg="white", bd=1, relief=tk.SOLID)
        frame.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
        
        # Título
        tk.Label(frame, text="Productos con Stock Bajo", font=("Arial", 14, "bold"), 
                bg="white", fg="#2C3E50").pack(pady=(15, 10), padx=15, anchor="w")
        
        # Contenido
        try:
            # Obtener productos con stock bajo
            productos = self.models['producto'].obtener_stock_bajo()
            
            if productos:
                # Crear tabla
                frame_tabla = tk.Frame(frame, bg="white")
                frame_tabla.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
                
                # Cabeceras
                tk.Label(frame_tabla, text="Producto", font=("Arial", 11, "bold"), 
                        bg="white", fg="#2C3E50").grid(row=0, column=0, sticky="w", padx=5, pady=5)
                tk.Label(frame_tabla, text="Stock", font=("Arial", 11, "bold"), 
                        bg="white", fg="#2C3E50").grid(row=0, column=1, sticky="w", padx=5, pady=5)
                tk.Label(frame_tabla, text="Mínimo", font=("Arial", 11, "bold"), 
                        bg="white", fg="#2C3E50").grid(row=0, column=2, sticky="w", padx=5, pady=5)
                
                # Datos
                for i, producto in enumerate(productos[:5], 1):  # Mostrar solo los primeros 5
                    nombre = producto[1]
                    stock = producto[4]
                    minimo = producto[5]
                    
                    tk.Label(frame_tabla, text=nombre, font=("Arial", 10), 
                            bg="white", fg="#2C3E50").grid(row=i, column=0, sticky="w", padx=5, pady=3)
                    tk.Label(frame_tabla, text=str(stock), font=("Arial", 10, "bold"), 
                            bg="white", fg="#E74C3C").grid(row=i, column=1, sticky="w", padx=5, pady=3)
                    tk.Label(frame_tabla, text=str(minimo), font=("Arial", 10), 
                            bg="white", fg="#2C3E50").grid(row=i, column=2, sticky="w", padx=5, pady=3)
                
                # Botón para ver todos
                if len(productos) > 5:
                    btn_ver_todos = tk.Button(frame, text="Ver todos", bg="#3498DB", fg="white",
                                            font=("Arial", 10), cursor="hand2")
                    btn_ver_todos.pack(pady=(0, 15))
            else:
                tk.Label(frame, text="No hay productos con stock bajo", 
                        bg="white", fg="#27AE60", font=("Arial", 12)).pack(pady=30)
                
        except Exception as e:
            tk.Label(frame, text=f"Error al cargar datos: {e}", 
                    bg="white", fg="#E74C3C").pack(pady=10, padx=15)
    
    def crear_widget_grafico_ventas(self, parent, row, col):
        """Crear widget de gráfico de ventas"""
        frame = tk.Frame(parent, bg="white", bd=1, relief=tk.SOLID)
        frame.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
        
        # Título
        tk.Label(frame, text="Ventas de los Últimos 7 Días", font=("Arial", 14, "bold"), 
                bg="white", fg="#2C3E50").pack(pady=(15, 10), padx=15, anchor="w")
        
        # Contenido
        try:
            # Obtener datos de ventas
            ventas_diarias = self.models['venta'].obtener_total_ventas_por_dia(7)
            
            if ventas_diarias:
                # Crear figura y ejes
                fig, ax = plt.subplots(figsize=(8, 4))
                fig.patch.set_facecolor('white')
                
                # Preparar datos
                fechas = [venta[0] for venta in ventas_diarias]
                totales = [float(venta[1]) for venta in ventas_diarias]
                
                # Crear gráfico de barras
                bars = ax.bar(fechas, totales, color='#3498DB')
                
                # Añadir etiquetas
                ax.set_xlabel('Fecha')
                ax.set_ylabel('Total (S/)')
                ax.set_title('Ventas Diarias')
                
                # Rotar etiquetas del eje x
                plt.xticks(rotation=45)
                
                # Añadir valores sobre las barras
                for bar in bars:
                    height = bar.get_height()
                    ax.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                           f'S/{height:.1f}', ha='center', va='bottom', rotation=0)
                
                # Ajustar layout
                plt.tight_layout()
                
                # Crear canvas para mostrar el gráfico
                canvas = FigureCanvasTkAgg(fig, master=frame)
                canvas.draw()
                canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
                
            else:
                tk.Label(frame, text="No hay datos de ventas para mostrar", 
                        bg="white", fg="#7F8C8D", font=("Arial", 12)).pack(pady=30)
                
        except Exception as e:
            tk.Label(frame, text=f"Error al cargar gráfico: {e}", 
                    bg="white", fg="#E74C3C").pack(pady=10, padx=15)
    
    def crear_widget_productos_vendidos(self, parent, row, col):
        """Crear widget de productos más vendidos"""
        frame = tk.Frame(parent, bg="white", bd=1, relief=tk.SOLID)
        frame.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
        
        # Título
        tk.Label(frame, text="Productos Más Vendidos", font=("Arial", 14, "bold"), 
                bg="white", fg="#2C3E50").pack(pady=(15, 10), padx=15, anchor="w")
        
        # Contenido
        try:
            # Obtener productos más vendidos
            productos = self.models['venta'].obtener_productos_mas_vendidos(5)
            
            if productos:
                # Crear tabla
                frame_tabla = tk.Frame(frame, bg="white")
                frame_tabla.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
                
                # Cabeceras
                tk.Label(frame_tabla, text="Producto", font=("Arial", 11, "bold"), 
                        bg="white", fg="#2C3E50").grid(row=0, column=0, sticky="w", padx=5, pady=5)
                tk.Label(frame_tabla, text="Cantidad", font=("Arial", 11, "bold"), 
                        bg="white", fg="#2C3E50").grid(row=0, column=1, sticky="w", padx=5, pady=5)
                tk.Label(frame_tabla, text="Total", font=("Arial", 11, "bold"), 
                        bg="white", fg="#2C3E50").grid(row=0, column=2, sticky="w", padx=5, pady=5)
                
                # Datos
                for i, producto in enumerate(productos, 1):
                    nombre = producto[0]
                    cantidad = producto[1]
                    total = float(producto[2])
                    
                    tk.Label(frame_tabla, text=nombre, font=("Arial", 10), 
                            bg="white", fg="#2C3E50").grid(row=i, column=0, sticky="w", padx=5, pady=3)
                    tk.Label(frame_tabla, text=str(cantidad), font=("Arial", 10), 
                            bg="white", fg="#2C3E50").grid(row=i, column=1, sticky="w", padx=5, pady=3)
                    tk.Label(frame_tabla, text=f"S/ {total:.2f}", font=("Arial", 10), 
                            bg="white", fg="#2C3E50").grid(row=i, column=2, sticky="w", padx=5, pady=3)
                
            else:
                tk.Label(frame, text="No hay datos de ventas para mostrar", 
                        bg="white", fg="#7F8C8D", font=("Arial", 12)).pack(pady=30)
                
        except Exception as e:
            tk.Label(frame, text=f"Error al cargar datos: {e}", 
                    bg="white", fg="#E74C3C").pack(pady=10, padx=15)