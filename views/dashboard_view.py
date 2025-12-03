#!/usr/bin/env python3
import tkinter as tk
from typing import Callable, Dict, List, Tuple


class DashboardView:
    def __init__(
        self,
        root: tk.Tk,
        stats: Dict[str, float],
        acciones: List[Tuple[str, str, Callable[[], None]]],
        obtener_notificaciones: Callable[[], List[str]],
        crear_tarjeta_stats: Callable[[tk.Widget, str, object, str, int], None],
    ):
        self.root = root
        self.frame_main = tk.Frame(self.root, bg="#ECF0F1")
        self.frame_main.pack(fill="both", expand=True)

        # Frame superior - Estadísticas
        frame_stats = tk.Frame(self.frame_main, bg="white", relief="raised", bd=2)
        frame_stats.pack(fill="x", pady=(0, 20))

        # Tarjetas de estadísticas (mismo orden)
        crear_tarjeta_stats(frame_stats, "Total Productos", stats['total_productos'], "📦", 0)
        crear_tarjeta_stats(frame_stats, "Ventas del Día", f"{stats['ventas_dia']:.2f}", "💰", 1)
        crear_tarjeta_stats(frame_stats, "Total Clientes", stats['total_clientes'], "👥", 2)
        crear_tarjeta_stats(frame_stats, "Stock Bajo", stats['stock_bajo'], "⚠️", 3)

        # Frame inferior - Acciones rápidas
        frame_acciones = tk.Frame(self.frame_main, bg="white", relief="raised", bd=2)
        frame_acciones.pack(fill="both", expand=True)

        tk.Label(
            frame_acciones,
            text="Acciones Rápidas",
            font=("Arial", 16, "bold"),
            bg="white",
            fg="#2C3E50",
        ).pack(pady=(10, 20))

        botones_frame = tk.Frame(frame_acciones, bg="white")
        botones_frame.pack()

        for i, (icono, texto, comando) in enumerate(acciones):
            fila = i // 4
            columna = i % 4

            btn_frame = tk.Frame(botones_frame, bg="#3498DB", relief="raised", bd=2, cursor="hand2")
            btn_frame.grid(row=fila, column=columna, padx=10, pady=10)

            btn = tk.Button(
                btn_frame,
                text=f"{icono}\n{texto}",
                command=comando,
                bg="#3498DB",
                fg="white",
                font=("Arial", 10, "bold"),
                width=12,
                height=3,
                bd=0,
                cursor="hand2",
            )
            btn.pack()

        # Panel de notificaciones
        frame_notif = tk.Frame(self.frame_main, bg="#F39C12", relief="raised", bd=2)
        frame_notif.pack(fill="x", pady=(20, 0), padx=20)

        tk.Label(
            frame_notif,
            text="📢 Notificaciones",
            font=("Arial", 14, "bold"),
            bg="#F39C12",
            fg="white",
        ).pack(pady=(10, 5))

        notificaciones = obtener_notificaciones()

        if notificaciones:
            for notif in notificaciones:
                tk.Label(
                    frame_notif,
                    text=f"• {notif}",
                    font=("Arial", 10),
                    bg="#F39C12",
                    fg="white",
                    justify="left",
                ).pack(anchor="w", padx=20)
        else:
            tk.Label(
                frame_notif,
                text="No hay notificaciones pendientes",
                font=("Arial", 10),
                bg="#F39C12",
                fg="white",
            ).pack(pady=5)


