import tkinter as tk
from tkinter import messagebox, ttk
from typing import Callable

from domain.entidades.usuario import Usuario
from servicios.autenticacion_servicio import AutenticacionServicio
from Vistas.ui.colors import Colors
from Vistas.ui.components import Card, SPACE_LG, SPACE_MD, form_field
from Vistas.ui.theme import FONT


class LoginFrame(ttk.Frame):
    """Pantalla de inicio de sesión — diseño centrado con tarjeta."""

    def __init__(
        self,
        parent: tk.Widget,
        auth: AutenticacionServicio,
        on_login: Callable[[Usuario], None],
        on_registro: Callable[[], None],
    ) -> None:
        super().__init__(parent, style="App.TFrame")
        self.auth = auth
        self.on_login = on_login
        self.on_registro = on_registro

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        centro = ttk.Frame(self, style="App.TFrame")
        centro.grid(row=0, column=0)

        # Marca institucional
        marca = tk.Frame(centro, bg=Colors.GRAY_50)
        marca.pack(pady=(0, SPACE_LG))
        logo = tk.Canvas(marca, width=56, height=56, bg=Colors.GRAY_50, highlightthickness=0)
        logo.pack()
        logo.create_oval(4, 4, 52, 52, fill=Colors.RED, outline="")
        logo.create_text(28, 28, text="U", fill=Colors.WHITE, font=(FONT, 20, "bold"))

        ttk.Label(centro, text="ULEAM Management System", style="Title.TLabel").pack(pady=(0, 4))
        ttk.Label(centro, text="Sistema de Nivelación Académica", style="Subtitle.TLabel").pack(pady=(0, SPACE_LG))

        card = Card(centro, title="Iniciar sesión")
        card.pack()

        self.var_cedula = tk.StringVar()
        self.var_contrasena = tk.StringVar()

        form_field(card.body, "Cédula", self.var_cedula, width=38)[0].pack(fill=tk.X)
        form_field(card.body, "Contraseña", self.var_contrasena, show="*", width=38)[0].pack(fill=tk.X)

        btns = ttk.Frame(card.body, style="Card.TFrame")
        btns.pack(fill=tk.X, pady=(SPACE_MD, 0))
        ttk.Button(btns, text="Iniciar sesión", style="Primary.TButton", command=self._login).pack(
            side=tk.LEFT, padx=(0, 8)
        )
        ttk.Button(btns, text="Crear cuenta", style="Secondary.TButton", command=self.on_registro).pack(side=tk.LEFT)

    def _login(self) -> None:
        try:
            usuario = self.auth.iniciar_sesion(
                self.var_cedula.get().strip(),
                self.var_contrasena.get(),
            )
            self.on_login(usuario)
        except ValueError as error:
            messagebox.showerror("Acceso denegado", str(error))
