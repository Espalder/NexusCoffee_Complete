#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk


class ConfigView:
    def __init__(self, root: tk.Tk,
                 on_volver,
                 on_guardar,
                 tema_var: tk.StringVar):
        self.root = root
        self.frame_config = tk.Frame(self.root, bg="#ECF0F1")
        self.frame_config.pack(fill="both", expand=True, padx=20, pady=20)

        btn_volver = tk.Button(self.frame_config, text="⬅ Volver al Dashboard",
                               command=on_volver,
                               bg="#95A5A6", fg="white", font=("Arial", 10, "bold"))
        btn_volver.pack(pady=10, padx=10, anchor="nw")

        tk.Label(self.frame_config, text="Configuración del Sistema",
                font=("Arial", 20, "bold"), bg="#ECF0F1", fg="#2C3E50").pack(pady=(0, 20))

        self.notebook = ttk.Notebook(self.frame_config)
        self.notebook.pack(fill="both", expand=True)

        self.frame_cafeteria = tk.Frame(self.notebook, bg="white")
        self.notebook.add(self.frame_cafeteria, text="Información de la Cafetería")

        self.frame_preferencias = tk.Frame(self.notebook, bg="white")
        self.notebook.add(self.frame_preferencias, text="Preferencias")

        self.frame_usuarios = tk.Frame(self.notebook, bg="white")
        self.notebook.add(self.frame_usuarios, text="Usuarios")

        # Preferencias
        tk.Label(self.frame_preferencias, text="Tema:", font=("Arial", 12), bg="white").grid(row=0, column=0, sticky="w", padx=20, pady=10)
        frame_tema = tk.Frame(self.frame_preferencias, bg="white")
        frame_tema.grid(row=0, column=1, sticky="w", padx=20, pady=10)
        tk.Radiobutton(frame_tema, text="Claro", variable=tema_var, value="claro", bg="white", font=("Arial", 12)).pack(side="left", padx=5)
        tk.Radiobutton(frame_tema, text="Oscuro", variable=tema_var, value="oscuro", bg="white", font=("Arial", 12)).pack(side="left", padx=5)

        # Campos de información de la cafetería
        tk.Label(self.frame_cafeteria, text="Nombre de la Cafetería:", font=("Arial", 12), bg="white").grid(row=0, column=0, sticky="w", padx=20, pady=10)
        self.entry_nombre_cafeteria = tk.Entry(self.frame_cafeteria, font=("Arial", 12), width=40)
        self.entry_nombre_cafeteria.grid(row=0, column=1, sticky="ew", padx=20, pady=10)

        tk.Label(self.frame_cafeteria, text="Dirección:", font=("Arial", 12), bg="white").grid(row=1, column=0, sticky="w", padx=20, pady=10)
        self.entry_direccion = tk.Entry(self.frame_cafeteria, font=("Arial", 12), width=40)
        self.entry_direccion.grid(row=1, column=1, sticky="ew", padx=20, pady=10)

        tk.Label(self.frame_cafeteria, text="Teléfono:", font=("Arial", 12), bg="white").grid(row=2, column=0, sticky="w", padx=20, pady=10)
        self.entry_telefono = tk.Entry(self.frame_cafeteria, font=("Arial", 12), width=40)
        self.entry_telefono.grid(row=2, column=1, sticky="ew", padx=20, pady=10)

        tk.Label(self.frame_cafeteria, text="Email:", font=("Arial", 12), bg="white").grid(row=3, column=0, sticky="w", padx=20, pady=10)
        self.entry_email = tk.Entry(self.frame_cafeteria, font=("Arial", 12), width=40)
        self.entry_email.grid(row=3, column=1, sticky="ew", padx=20, pady=10)

        tk.Label(self.frame_cafeteria, text="RUC:", font=("Arial", 12), bg="white").grid(row=4, column=0, sticky="w", padx=20, pady=10)
        self.entry_ruc = tk.Entry(self.frame_cafeteria, font=("Arial", 12), width=40)
        self.entry_ruc.grid(row=4, column=1, sticky="ew", padx=20, pady=10)

        self.frame_cafeteria.grid_columnconfigure(1, weight=1)

        # Preferencias adicionales
        tk.Label(self.frame_preferencias, text="Símbolo de Moneda:", font=("Arial", 12), bg="white").grid(row=1, column=0, sticky="w", padx=20, pady=10)
        self.entry_moneda = tk.Entry(self.frame_preferencias, font=("Arial", 12), width=10)
        self.entry_moneda.grid(row=1, column=1, sticky="w", padx=20, pady=10)

        tk.Label(self.frame_preferencias, text="Stock Mínimo Predeterminado:", font=("Arial", 12), bg="white").grid(row=2, column=0, sticky="w", padx=20, pady=10)
        self.entry_stock_minimo = tk.Entry(self.frame_preferencias, font=("Arial", 12), width=10)
        self.entry_stock_minimo.grid(row=2, column=1, sticky="w", padx=20, pady=10)

        tk.Label(self.frame_preferencias, text="Respaldo Automático:", font=("Arial", 12), bg="white").grid(row=3, column=0, sticky="w", padx=20, pady=10)
        self.combo_respaldo = ttk.Combobox(self.frame_preferencias, values=["diario", "semanal", "mensual", "nunca"], font=("Arial", 12), width=15)
        self.combo_respaldo.grid(row=3, column=1, sticky="w", padx=20, pady=10)

        # Botón guardar
        frame_botones = tk.Frame(self.frame_config, bg="#ECF0F1")
        frame_botones.pack(fill="x", pady=20)
        tk.Button(frame_botones, text="Guardar Configuración",
                 command=on_guardar, bg="#27AE60", fg="white",
                 font=("Arial", 12, "bold")).pack(side="right", padx=5)


