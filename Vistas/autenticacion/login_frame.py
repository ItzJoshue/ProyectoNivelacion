import tkinter as tk
from tkinter import messagebox, ttk
from typing import Callable

from domain.entidades.usuario import Usuario
from servicios.autenticacion_servicio import AutenticacionServicio


class LoginFrame(ttk.Frame):
    """Pantalla de inicio de sesión."""

    def __init__(
        self,
        parent: tk.Widget,
        auth: AutenticacionServicio,
        on_login: Callable[[Usuario], None],
        on_registro: Callable[[], None],
    ) -> None:
        super().__init__(parent, padding=30)
        self.auth = auth
        self.on_login = on_login
        self.on_registro = on_registro

        ttk.Label(self, text="ULEAM Management System", font=("Segoe UI", 18, "bold")).pack(pady=(0, 4))
        ttk.Label(self, text="Inicio de sesión").pack(pady=(0, 20))

        form = ttk.Frame(self)
        form.pack()

        self.var_cedula = tk.StringVar()
        self.var_contrasena = tk.StringVar()

        ttk.Label(form, text="Cédula:").grid(row=0, column=0, sticky=tk.W, pady=6)
        ttk.Entry(form, textvariable=self.var_cedula, width=32).grid(row=0, column=1, padx=8, pady=6)

        ttk.Label(form, text="Contraseña:").grid(row=1, column=0, sticky=tk.W, pady=6)
        ttk.Entry(form, textvariable=self.var_contrasena, show="*", width=32).grid(
            row=1, column=1, padx=8, pady=6
        )

        btns = ttk.Frame(self)
        btns.pack(pady=20)
        ttk.Button(btns, text="Iniciar sesión", command=self._login).pack(side=tk.LEFT, padx=6)
        ttk.Button(btns, text="Registrarse", command=self.on_registro).pack(side=tk.LEFT, padx=6)

    def _login(self) -> None:
        try:
            usuario = self.auth.iniciar_sesion(
                self.var_cedula.get().strip(),
                self.var_contrasena.get(),
            )
            self.on_login(usuario)
        except ValueError as error:
            messagebox.showerror("Acceso denegado", str(error))
