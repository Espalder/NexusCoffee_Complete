#!/usr/bin/env python3
import tkinter as tk


class ReportesHomeView:
    def __init__(self, root: tk.Tk, acciones):
        self.root = root
        self.frame_reportes = tk.Frame(self.root, bg="#ECF0F1")
        self.frame_reportes.pack(fill="both", expand=True, padx=20, pady=20)

        btn_volver = tk.Button(self.frame_reportes, text="⬅ Volver al Dashboard",
                               command=acciones.get('volver'),
                               bg="#95A5A6", fg="white", font=("Arial", 10, "bold"))
        btn_volver.pack(pady=10, padx=10, anchor="nw")

        tk.Label(self.frame_reportes, text="Reportes y Estadísticas",
                font=("Arial", 20, "bold"), bg="#ECF0F1", fg="#2C3E50").pack(pady=(0, 20))

        frame_botones = tk.Frame(self.frame_reportes, bg="white", relief="raised", bd=2)
        frame_botones.pack(fill="both", expand=True, padx=20, pady=20)

        botones = [
            ("📊", "Reporte de Ventas", acciones.get('ventas')),
            ("📦", "Reporte de Inventario", acciones.get('inventario')),
            ("👥", "Reporte de Clientes", acciones.get('clientes')),
            ("💰", "Reporte de Ingresos", acciones.get('ingresos')),
            ("📉", "Productos Menos Vendidos", acciones.get('menos_vendidos')),
            ("📈", "Tendencias", acciones.get('tendencias')),
        ]

        for i, (icono, texto, comando) in enumerate(botones):
            fila = i // 3
            columna = i % 3
            btn_frame = tk.Frame(frame_botones, bg="#3498DB", relief="raised", bd=2, cursor="hand2")
            btn_frame.grid(row=fila, column=columna, padx=20, pady=20, sticky="nsew")
            btn = tk.Button(btn_frame, text=f"{icono}\n{texto}", command=comando,
                            bg="#3498DB", fg="white", font=("Arial", 12, "bold"),
                            width=15, height=3, bd=0, cursor="hand2")
            btn.pack(padx=10, pady=10)
            frame_botones.grid_rowconfigure(fila, weight=1)
            frame_botones.grid_columnconfigure(columna, weight=1)


