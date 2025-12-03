#!/usr/bin/env python3
"""
Módulo para generar gráficos para Nexus Café
"""

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import pandas as pd
import datetime

class ChartGenerator:
    def __init__(self):
        pass
    
    def crear_grafico_ventas_bar(self, parent, ventas_data, title="Ventas"):
        """Crea un gráfico de barras para las ventas"""
        try:
            # Limpiar frame
            for widget in parent.winfo_children():
                widget.destroy()
            
            # Crear figura y ejes
            fig, ax = plt.subplots(figsize=(8, 4))
            fig.patch.set_facecolor('white')
            
            # Preparar datos
            fechas = [venta[0].strftime("%d/%m") for venta in ventas_data]
            montos = [float(venta[1]) for venta in ventas_data]
            
            # Crear gráfico de barras
            bars = ax.bar(fechas, montos, color='#3498DB')
            
            # Añadir etiquetas
            ax.set_ylabel('Monto (S/)')
            ax.set_title(title)
            
            # Rotar etiquetas del eje x
            plt.xticks(rotation=45)
            
            # Añadir valores sobre las barras
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                       f'S/{height:.1f}', ha='center', va='bottom', rotation=0)
            
            # Ajustar layout
            plt.tight_layout()
            
            # Mostrar gráfico en tkinter
            canvas = FigureCanvasTkAgg(fig, master=parent)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)
            
            return True
            
        except Exception as e:
            print(f"Error al crear gráfico de barras: {e}")
            return False
    
    def crear_grafico_ventas_line(self, parent, ventas_data, title="Ventas"):
        """Crea un gráfico de líneas para las ventas"""
        try:
            # Limpiar frame
            for widget in parent.winfo_children():
                widget.destroy()
            
            # Crear figura y ejes
            fig, ax = plt.subplots(figsize=(8, 4))
            fig.patch.set_facecolor('white')
            
            # Preparar datos
            fechas = [venta[0].strftime("%d/%m") for venta in ventas_data]
            montos = [float(venta[1]) for venta in ventas_data]
            
            # Crear gráfico de líneas
            ax.plot(fechas, montos, marker='o', color='#E74C3C', linewidth=2, markersize=8)
            
            # Añadir etiquetas
            ax.set_ylabel('Monto (S/)')
            ax.set_title(title)
            
            # Rotar etiquetas del eje x
            plt.xticks(rotation=45)
            
            # Añadir valores sobre los puntos
            for i, (fecha, monto) in enumerate(zip(fechas, montos)):
                ax.annotate(f'S/{monto:.1f}', (i, monto), textcoords="offset points", 
                           xytext=(0,10), ha='center')
            
            # Ajustar layout
            plt.tight_layout()
            
            # Mostrar gráfico en tkinter
            canvas = FigureCanvasTkAgg(fig, master=parent)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)
            
            return True
            
        except Exception as e:
            print(f"Error al crear gráfico de líneas: {e}")
            return False
    
    def crear_grafico_productos_pie(self, parent, productos_data, title="Productos"):
        """Crea un gráfico circular para los productos"""
        try:
            # Limpiar frame
            for widget in parent.winfo_children():
                widget.destroy()
            
            # Crear figura y ejes
            fig, ax = plt.subplots(figsize=(8, 6))
            fig.patch.set_facecolor('white')
            
            # Preparar datos
            nombres = [producto[0] for producto in productos_data]
            cantidades = [producto[1] for producto in productos_data]
            
            # Crear gráfico circular
            wedges, texts, autotexts = ax.pie(cantidades, labels=nombres, autopct='%1.1f%%',
                                          startangle=90, colors=plt.cm.tab20.colors)
            
            # Asegurar que los textos sean legibles
            plt.setp(autotexts, size=10, weight="bold", color="white")
            ax.set_title(title, weight='bold')
            
            # Ajustar layout
            plt.tight_layout()
            
            # Mostrar gráfico en tkinter
            canvas = FigureCanvasTkAgg(fig, master=parent)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)
            
            return True
            
        except Exception as e:
            print(f"Error al crear gráfico circular: {e}")
            return False
    
    def crear_grafico_productos_horizontal(self, parent, productos_data, title="Productos"):
        """Crea un gráfico de barras horizontal para los productos"""
        try:
            # Limpiar frame
            for widget in parent.winfo_children():
                widget.destroy()
            
            # Crear figura y ejes
            fig, ax = plt.subplots(figsize=(8, 6))
            fig.patch.set_facecolor('white')
            
            # Preparar datos
            nombres = [producto[0] for producto in productos_data]
            cantidades = [producto[1] for producto in productos_data]
            
            # Crear gráfico de barras horizontal
            bars = ax.barh(nombres, cantidades, color='#2ECC71')
            
            # Añadir etiquetas
            ax.set_xlabel('Cantidad')
            ax.set_title(title)
            
            # Añadir valores a las barras
            for i, v in enumerate(cantidades):
                ax.text(v + 0.1, i, str(v), color='black', fontweight='bold')
            
            # Ajustar layout
            plt.tight_layout()
            
            # Mostrar gráfico en tkinter
            canvas = FigureCanvasTkAgg(fig, master=parent)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)
            
            return True
            
        except Exception as e:
            print(f"Error al crear gráfico de barras horizontal: {e}")
            return False