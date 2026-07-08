import tkinter as tk
from tkinter import messagebox, ttk
from typing import Callable

from domain.entidades.usuario import Usuario
from servicios.contenedor import ContenedorAplicacion
from Vistas.ui.colors import Colors
from Vistas.ui.components import Card, SPACE_LG, SPACE_MD, SPACE_XL, form_field
from Vistas.ui.icons import dibujar_logo
from Vistas.ui.theme import SUBTITULO_INSTITUCION, TITULO_APP


class LoginFrame(ttk.Frame):
    """Pantalla de inicio de sesión — diseño centrado con tarjeta."""

    def __init__(
        self,
        parent: tk.Widget,
        contenedor: ContenedorAplicacion,
        on_login: Callable[[Usuario], None],
        on_registro: Callable[[], None],
    ) -> None:
        super().__init__(parent, style="App.TFrame")
        self.contenedor = contenedor
        self.on_login = on_login
        self.on_registro = on_registro

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        centro = ttk.Frame(self, style="App.TFrame", padding=SPACE_XL)
        centro.grid(row=0, column=0)

        marca = tk.Frame(centro, bg=Colors.BG_APP)
        marca.pack(pady=(0, SPACE_LG))
        logo = tk.Canvas(marca, width=64, height=64, bg=Colors.BG_APP, highlightthickness=0)
        logo.pack()
        dibujar_logo(logo, 64, bg=Colors.BG_APP)

        ttk.Label(centro, text=TITULO_APP, style="Title.TLabel").pack(pady=(0, SPACE_MD))
        ttk.Label(centro, text=SUBTITULO_INSTITUCION, style="Subtitle.TLabel").pack(pady=(0, SPACE_XL))

        card = Card(centro, title="Iniciar sesión")
        card.pack()

        self.var_cedula = tk.StringVar()
        self.var_contrasena = tk.StringVar()

        form_field(card.body, "Cédula", self.var_cedula, width=36)[0].pack(fill=tk.X)
        form_field(card.body, "Contraseña", self.var_contrasena, show="•", width=36)[0].pack(fill=tk.X)

        btns = ttk.Frame(card.body, style="Card.TFrame")
        btns.pack(fill=tk.X, pady=(SPACE_MD, 0))
        ttk.Button(btns, text="Iniciar sesión", style="Primary.TButton", command=self._login).pack(
            side=tk.LEFT, padx=(0, SPACE_MD)
        )
        ttk.Button(btns, text="Crear cuenta", style="Secondary.TButton", command=self.on_registro).pack(side=tk.LEFT)

    def _login(self) -> None:
        try:
            usuario = self.contenedor.iniciar_sesion(
                self.var_cedula.get().strip(),
                self.var_contrasena.get(),
            )
            self.on_login(usuario)
        except ValueError as error:
            messagebox.showerror("Acceso denegado", str(error))
