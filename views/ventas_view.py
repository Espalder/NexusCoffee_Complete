#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk


class VentasView:
    def __init__(self, root: tk.Tk, on_volver, on_nueva_venta, on_eliminar_venta, on_buscar):
        self.root = root

        self.frame_ventas = tk.Frame(self.root, bg="#ECF0F1")
        self.frame_ventas.pack(fill="both", expand=True, padx=20, pady=20)

        btn_volver = tk.Button(self.frame_ventas, text="⬅ Volver al Dashboard", command=on_volver,
                               bg="#95A5A6", fg="white", font=("Arial", 10, "bold"))
        btn_volver.pack(pady=10, padx=10, anchor="nw")

        tk.Label(self.frame_ventas, text="Gestión de Ventas",
                 font=("Arial", 20, "bold"), bg="#ECF0F1", fg="#2C3E50").pack(pady=(0, 20))

        frame_controles = tk.Frame(self.frame_ventas, bg="#ECF0F1")
        frame_controles.pack(fill="x", pady=(0, 20))

        tk.Button(frame_controles, text="➕ Nueva Venta", command=on_nueva_venta,
                  bg="#27AE60", fg="white", font=("Arial", 10, "bold")).pack(side="left", padx=5)
        tk.Button(frame_controles, text="🗑️ Eliminar Venta", command=on_eliminar_venta,
                  bg="#E74C3C", fg="white", font=("Arial", 10, "bold")).pack(side="left", padx=5)

        frame_busqueda = tk.Frame(self.frame_ventas, bg="#ECF0F1")
        frame_busqueda.pack(fill="x", pady=(0, 20))

        tk.Label(frame_busqueda, text="Buscar:", bg="#ECF0F1", font=("Arial", 12)).pack(side="left", padx=(0, 10))
        self.entry_busqueda = tk.Entry(frame_busqueda, font=("Arial", 12), width=30)
        self.entry_busqueda.pack(side="left", padx=(0, 10))
        tk.Button(frame_busqueda, text="🔍 Buscar", command=on_buscar,
                  bg="#95A5A6", fg="white", font=("Arial", 10, "bold")).pack(side="left")

        frame_tabla = tk.Frame(self.frame_ventas, bg="#ECF0F1")
        frame_tabla.pack(fill="both", expand=True)

        scrollbar_y = tk.Scrollbar(frame_tabla)
        scrollbar_y.pack(side="right", fill="y")

        scrollbar_x = tk.Scrollbar(frame_tabla, orient="horizontal")
        scrollbar_x.pack(side="bottom", fill="x")

        self.tabla_ventas = ttk.Treeview(frame_tabla,
                                         columns=("ID", "Cliente", "Total", "Fecha", "Usuario"),
                                         yscrollcommand=scrollbar_y.set,
                                         xscrollcommand=scrollbar_x.set,
                                         selectmode="extended")

        self.tabla_ventas.heading("#0", text="")
        self.tabla_ventas.heading("ID", text="ID", command=lambda: self._ordenar_columna(self.tabla_ventas, "ID", False))
        self.tabla_ventas.heading("Cliente", text="Cliente", command=lambda: self._ordenar_columna(self.tabla_ventas, "Cliente", False))
        self.tabla_ventas.heading("Total", text="Total", command=lambda: self._ordenar_columna(self.tabla_ventas, "Total", False))
        self.tabla_ventas.heading("Fecha", text="Fecha", command=lambda: self._ordenar_columna(self.tabla_ventas, "Fecha", False))
        self.tabla_ventas.heading("Usuario", text="Usuario", command=lambda: self._ordenar_columna(self.tabla_ventas, "Usuario", False))

        self.tabla_ventas.column("#0", width=0, stretch=False)
        self.tabla_ventas.column("ID", width=60, anchor="center")
        self.tabla_ventas.column("Cliente", width=200, anchor="w")
        self.tabla_ventas.column("Total", width=100, anchor="center")
        self.tabla_ventas.column("Fecha", width=150, anchor="center")
        self.tabla_ventas.column("Usuario", width=120, anchor="center")

        self.tabla_ventas.pack(fill="both", expand=True)
        scrollbar_y.config(command=self.tabla_ventas.yview)
        scrollbar_x.config(command=self.tabla_ventas.xview)

    def _ordenar_columna(self, tree, col, reverse):
        try:
            def keyfunc(item_id):
                val = tree.set(item_id, col)
                s = str(val).replace("S/", "").replace(",", "").strip()
                try:
                    return float(s)
                except ValueError:
                    return str(val).lower()
            datos = [(keyfunc(i), i) for i in tree.get_children("")]
            datos.sort(key=lambda t: t[0], reverse=reverse)
            for idx, (_, item_id) in enumerate(datos):
                tree.move(item_id, "", idx)
            tree.heading(col, command=lambda: self._ordenar_columna(tree, col, not reverse))
        except Exception:
            datos = [(tree.set(i, col), i) for i in tree.get_children("")]
            datos.sort(key=lambda t: str(t[0]).lower(), reverse=reverse)
            for idx, (_, item_id) in enumerate(datos):
                tree.move(item_id, "", idx)
            tree.heading(col, command=lambda: self._ordenar_columna(tree, col, not reverse))


