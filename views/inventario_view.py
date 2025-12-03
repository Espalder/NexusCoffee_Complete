#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk


class InventarioView:
    def __init__(self,
                 root: tk.Tk,
                 on_volver,
                 on_agregar_producto,
                 on_editar_producto,
                 on_eliminar_producto,
                 on_actualizar_stock,
                 on_buscar_producto):
        self.root = root

        self.frame_inventario = tk.Frame(self.root, bg="#ECF0F1")
        self.frame_inventario.pack(fill="both", expand=True, padx=20, pady=20)

        btn_volver = tk.Button(self.frame_inventario, text="⬅ Volver al Dashboard",
                               command=on_volver,
                               bg="#95A5A6", fg="white", font=("Arial", 10, "bold"))
        btn_volver.pack(pady=10, padx=10, anchor="nw")

        tk.Label(self.frame_inventario, text="Gestión de Inventario",
                font=("Arial", 20, "bold"), bg="#ECF0F1", fg="#2C3E50").pack(pady=(0, 20))

        frame_controles = tk.Frame(self.frame_inventario, bg="#ECF0F1")
        frame_controles.pack(fill="x", pady=(0, 20))

        tk.Button(frame_controles, text="➕ Agregar Producto",
                 command=on_agregar_producto, bg="#27AE60", fg="white",
                 font=("Arial", 10, "bold")).pack(side="left", padx=5)

        tk.Button(frame_controles, text="✏️ Editar Producto",
                 command=on_editar_producto, bg="#3498DB", fg="white",
                 font=("Arial", 10, "bold")).pack(side="left", padx=5)

        tk.Button(frame_controles, text="🗑️ Eliminar Producto",
                 command=on_eliminar_producto, bg="#E74C3C", fg="white",
                 font=("Arial", 10, "bold")).pack(side="left", padx=5)

        tk.Button(frame_controles, text="📋 Actualizar Stock",
                 command=on_actualizar_stock, bg="#F39C12", fg="white",
                 font=("Arial", 10, "bold")).pack(side="left", padx=5)

        frame_busqueda = tk.Frame(self.frame_inventario, bg="#ECF0F1")
        frame_busqueda.pack(fill="x", pady=(0, 20))

        tk.Label(frame_busqueda, text="Buscar:", bg="#ECF0F1", font=("Arial", 12)).pack(side="left", padx=(0, 10))
        self.entry_busqueda = tk.Entry(frame_busqueda, font=("Arial", 12), width=30)
        self.entry_busqueda.pack(side="left", padx=(0, 10))
        tk.Button(frame_busqueda, text="🔍 Buscar",
                 command=on_buscar_producto, bg="#95A5A6", fg="white",
                 font=("Arial", 10, "bold")).pack(side="left")

        frame_tabla = tk.Frame(self.frame_inventario, bg="#ECF0F1")
        frame_tabla.pack(fill="both", expand=True)

        scrollbar_y = tk.Scrollbar(frame_tabla)
        scrollbar_y.pack(side="right", fill="y")

        scrollbar_x = tk.Scrollbar(frame_tabla, orient="horizontal")
        scrollbar_x.pack(side="bottom", fill="x")

        self.tabla_productos = ttk.Treeview(frame_tabla,
                                            columns=("ID", "Nombre", "Categoría", "Precio", "Stock", "Stock Mínimo"),
                                            yscrollcommand=scrollbar_y.set,
                                            xscrollcommand=scrollbar_x.set,
                                            selectmode="extended")

        self.tabla_productos.heading("#0", text="")
        self.tabla_productos.heading("ID", text="ID", command=lambda: self._ordenar_columna(self.tabla_productos, "ID", False))
        self.tabla_productos.heading("Nombre", text="Nombre", command=lambda: self._ordenar_columna(self.tabla_productos, "Nombre", False))
        self.tabla_productos.heading("Categoría", text="Categoría", command=lambda: self._ordenar_columna(self.tabla_productos, "Categoría", False))
        self.tabla_productos.heading("Precio", text="Precio", command=lambda: self._ordenar_columna(self.tabla_productos, "Precio", False))
        self.tabla_productos.heading("Stock", text="Stock", command=lambda: self._ordenar_columna(self.tabla_productos, "Stock", False))
        self.tabla_productos.heading("Stock Mínimo", text="Stock Mínimo", command=lambda: self._ordenar_columna(self.tabla_productos, "Stock Mínimo", False))

        self.tabla_productos.column("#0", width=0, stretch=False)
        self.tabla_productos.column("ID", width=50, anchor="center")
        self.tabla_productos.column("Nombre", width=200, anchor="w")
        self.tabla_productos.column("Categoría", width=100, anchor="center")
        self.tabla_productos.column("Precio", width=80, anchor="center")
        self.tabla_productos.column("Stock", width=80, anchor="center")
        self.tabla_productos.column("Stock Mínimo", width=100, anchor="center")

        self.tabla_productos.pack(fill="both", expand=True)
        scrollbar_y.config(command=self.tabla_productos.yview)
        scrollbar_x.config(command=self.tabla_productos.xview)

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


