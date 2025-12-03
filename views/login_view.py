#!/usr/bin/env python3
import tkinter as tk
from tkinter import messagebox
from typing import Callable


class LoginView:
    def __init__(self, root: tk.Tk, on_submit: Callable[[str, str], None]):
        self.root = root
        self.on_submit = on_submit

        self.frame_login = tk.Frame(self.root, bg="#34495E", padx=50, pady=50)
        self.frame_login.place(relx=0.5, rely=0.5, anchor="center")

        titulo = tk.Label(
            self.frame_login,
            text="NEXUS CAFÉ",
            font=("Arial", 24, "bold"),
            fg="#E67E22",
            bg="#34495E",
        )
        titulo.pack(pady=(0, 30))

        logo_frame = tk.Frame(self.frame_login, bg="#34495E", width=100, height=100)
        logo_frame.pack(pady=(0, 20))
        logo_label = tk.Label(logo_frame, text="☕", font=("Arial", 48), bg="#34495E", fg="#E67E22")
        logo_label.pack()

        tk.Label(self.frame_login, text="Usuario:", font=("Arial", 12), bg="#34495E", fg="white").pack(anchor="w")
        self.entry_usuario = tk.Entry(self.frame_login, font=("Arial", 12), width=25)
        self.entry_usuario.pack(pady=(5, 15))

        tk.Label(self.frame_login, text="Contraseña:", font=("Arial", 12), bg="#34495E", fg="white").pack(anchor="w")
        self.entry_password = tk.Entry(self.frame_login, font=("Arial", 12), width=25, show="*")
        self.entry_password.pack(pady=(5, 20))

        btn_login = tk.Button(
            self.frame_login,
            text="Iniciar Sesión",
            command=self._submit,
            bg="#E67E22",
            fg="white",
            font=("Arial", 12, "bold"),
            width=20,
            cursor="hand2",
        )
        btn_login.pack(pady=10)

        info = tk.Label(
            self.frame_login,
            text="Usuario: admin | Contraseña: admin123",
            font=("Arial", 10),
            bg="#34495E",
            fg="#BDC3C7",
        )
        info.pack(pady=(20, 0))

        self.root.bind('<Return>', lambda e: self._submit())

    def _submit(self):
        usuario = self.entry_usuario.get()
        password = self.entry_password.get()
        if not usuario or not password:
            messagebox.showerror("Error", "Por favor complete todos los campos")
            return
        self.on_submit(usuario, password)


