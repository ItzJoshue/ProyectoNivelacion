"""Layout principal tipo dashboard — barra superior + sidebar + contenido."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk
from typing import Callable

from Vistas.ui.colors import Colors
from Vistas.ui.components import SPACE_LG, Sidebar, TopBar


class DashboardShell(ttk.Frame):
    """
    Shell responsive con grid:
    - Fila 0: TopBar
    - Fila 1, Col 0: Sidebar
    - Fila 1, Col 1: Área principal (scrollable)
    """

    SIDEBAR_WIDTH = 260

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

        self._canvas = tk.Canvas(
            self._main,
            highlightthickness=0,
            bg=Colors.GRAY_50,
            borderwidth=0,
        )
        self._vsb = ttk.Scrollbar(
            self._main,
            orient=tk.VERTICAL,
            command=self._canvas.yview,
            style="Modern.Vertical.TScrollbar",
        )
        self._canvas.configure(yscrollcommand=self._vsb.set)
        self._canvas.grid(row=0, column=0, sticky="nsew")
        self._vsb.grid(row=0, column=1, sticky="ns")

        self.contenido = ttk.Frame(self._canvas, style="Content.TFrame")
        self._canvas_window = self._canvas.create_window((0, 0), window=self.contenido, anchor="nw")
        self.contenido.columnconfigure(0, weight=1)
        self.contenido.rowconfigure(0, weight=1)

        self.contenido.bind("<Configure>", self._actualizar_scrollregion)
        self._canvas.bind("<Configure>", self._ajustar_ancho_contenido)
        self._canvas.bind("<Enter>", self._activar_scroll_rueda)
        self._canvas.bind("<Leave>", self._desactivar_scroll_rueda)
        self.contenido.bind("<Enter>", self._activar_scroll_rueda)
        self.contenido.bind("<Leave>", self._desactivar_scroll_rueda)

    def _actualizar_scrollregion(self, _event=None) -> None:
        self._canvas.configure(scrollregion=self._canvas.bbox("all"))

    def _ajustar_ancho_contenido(self, event: tk.Event) -> None:
        self._canvas.itemconfigure(self._canvas_window, width=event.width)

    def _activar_scroll_rueda(self, _event=None) -> None:
        self._canvas.bind_all("<MouseWheel>", self._scroll_rueda)
        self._canvas.bind_all("<Button-4>", self._scroll_rueda_linux)
        self._canvas.bind_all("<Button-5>", self._scroll_rueda_linux)

    def _desactivar_scroll_rueda(self, _event=None) -> None:
        self._canvas.unbind_all("<MouseWheel>")
        self._canvas.unbind_all("<Button-4>")
        self._canvas.unbind_all("<Button-5>")

    def _scroll_rueda(self, event: tk.Event) -> None:
        widget = event.widget
        while widget:
            if widget.winfo_class() == "Treeview":
                return
            widget = widget.master
        self._canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _scroll_rueda_linux(self, event: tk.Event) -> None:
        widget = event.widget
        while widget:
            if widget.winfo_class() == "Treeview":
                return
            widget = widget.master
        delta = -1 if event.num == 4 else 1
        self._canvas.yview_scroll(delta, "units")

    def limpiar_contenido(self) -> None:
        for w in self.contenido.winfo_children():
            w.destroy()
