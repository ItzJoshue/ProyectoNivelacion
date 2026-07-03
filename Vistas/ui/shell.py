"""Layout principal tipo dashboard — barra superior + sidebar + contenido."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk
from typing import Callable

from Vistas.ui.components import SPACE_LG, Sidebar, TopBar


class DashboardShell(ttk.Frame):
    """
    Shell responsive con grid:
    - Fila 0: TopBar
    - Fila 1, Col 0: Sidebar
    - Fila 1, Col 1: Área principal (scrollable)
    """

    SIDEBAR_WIDTH = 240

    def __init__(
        self,
        parent: tk.Widget,
        *,
        titulo: str,
        usuario: str,
        rol: str,
        menu_titulo: str,
        on_logout: Callable[[], None],
        root: tk.Tk | None = None,
    ) -> None:
        super().__init__(parent, style="App.TFrame")
        self.columnconfigure(1, weight=1)
        self.rowconfigure(1, weight=1)

        self.topbar = TopBar(self, titulo, usuario, rol, on_logout, root=root)
        self.topbar.grid(row=0, column=0, columnspan=2, sticky="ew")

        self.sidebar = Sidebar(self, titulo=menu_titulo)
        self.sidebar.grid(row=1, column=0, sticky="ns")

        self._main = ttk.Frame(self, style="Content.TFrame", padding=SPACE_LG)
        self._main.grid(row=1, column=1, sticky="nsew")
        self._main.columnconfigure(0, weight=1)
        self._main.rowconfigure(0, weight=1)

        self.contenido = ttk.Frame(self._main, style="Content.TFrame")
        self.contenido.grid(row=0, column=0, sticky="nsew")
        self.contenido.columnconfigure(0, weight=1)
        self.contenido.rowconfigure(0, weight=1)

    def limpiar_contenido(self) -> None:
        for w in self.contenido.winfo_children():
            w.destroy()
