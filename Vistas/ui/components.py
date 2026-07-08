"""Componentes visuales reutilizables — solo presentación, sin lógica de negocio."""

from __future__ import annotations

import tkinter as tk
from datetime import datetime
from tkinter import ttk
from typing import Callable

from Vistas.ui.colors import Colors
from Vistas.ui.icons import _tipo_nav, dibujar_boton_ventana, dibujar_icono_nav, dibujar_logo
from Vistas.ui.theme import FONT, SUBTITULO_INSTITUCION


# ── Espaciado ───────────────────────────────────────────────────────────
SPACE_XS = 4
SPACE_SM = 8
SPACE_MD = 16
SPACE_LG = 24
SPACE_XL = 32


class Card(tk.Frame):
    """Tarjeta con borde suave, fondo blanco y padding amplio."""

    def __init__(self, parent: tk.Widget, title: str | None = None, **kwargs) -> None:
        super().__init__(
            parent,
            bg=Colors.WHITE,
            highlightbackground=Colors.BORDER_SOFT,
            highlightthickness=1,
            **kwargs,
        )
        self._inner = ttk.Frame(self, style="Card.TFrame", padding=SPACE_LG)
        self._inner.pack(fill=tk.BOTH, expand=True)

        self._title_label: ttk.Label | None = None
        if title:
            self._title_label = ttk.Label(self._inner, text=title, style="CardTitle.TLabel")
            self._title_label.pack(anchor=tk.W, pady=(0, SPACE_MD))

        self.body = ttk.Frame(self._inner, style="Card.TFrame")
        self.body.pack(fill=tk.BOTH, expand=True)

    def set_title(self, title: str) -> None:
        if self._title_label is not None:
            self._title_label.configure(text=title)


def page_header(parent: tk.Widget, title: str, subtitle: str | None = None) -> ttk.Frame:
    """Encabezado de página con jerarquía tipográfica."""
    frame = ttk.Frame(parent, style="Content.TFrame", padding=(0, 0, 0, SPACE_LG))
    ttk.Label(frame, text=title, style="PageTitle.TLabel").pack(anchor=tk.W)
    if subtitle:
        ttk.Label(frame, text=subtitle, style="Muted.TLabel").pack(anchor=tk.W, pady=(SPACE_SM, 0))
    return frame


def form_field(
    parent: tk.Widget,
    label: str,
    textvariable: tk.StringVar | None = None,
    *,
    show: str | None = None,
    width: int = 42,
    combobox: bool = False,
    readonly: bool = False,
    values: list[str] | None = None,
) -> tuple[ttk.Frame, ttk.Entry | ttk.Combobox]:
    """Label encima del campo — nunca al lado."""
    container = ttk.Frame(parent, style="Card.TFrame")
    ttk.Label(container, text=label, style="Field.TLabel").pack(anchor=tk.W)

    if combobox:
        state = "readonly" if readonly else "normal"
        widget: ttk.Entry | ttk.Combobox = ttk.Combobox(
            container,
            textvariable=textvariable,
            style="Modern.TCombobox",
            width=width,
            state=state,
            values=values or [],
        )
    else:
        widget = ttk.Entry(
            container,
            textvariable=textvariable,
            style="Modern.TEntry",
            width=width,
            show=show,
        )

    widget.pack(fill=tk.X, pady=(SPACE_XS, SPACE_MD))
    return container, widget


def styled_text(parent: tk.Widget, **kwargs) -> tk.Text:
    """Área de texto con apariencia moderna."""
    defaults = dict(
        font=(FONT, 11),
        bg=Colors.WHITE,
        fg=Colors.TEXT_PRIMARY,
        relief="flat",
        highlightthickness=1,
        highlightbackground=Colors.BORDER,
        highlightcolor=Colors.PRIMARY,
        padx=SPACE_MD,
        pady=SPACE_MD,
        insertbackground=Colors.TEXT_PRIMARY,
        selectbackground=Colors.PRIMARY_SOFT,
        selectforeground=Colors.TEXT_PRIMARY,
        borderwidth=0,
    )
    defaults.update(kwargs)
    return tk.Text(parent, **defaults)


def create_treeview(
    parent: tk.Widget,
    columns: tuple[str, ...],
    headings: dict[str, str] | None = None,
    *,
    height: int = 12,
    col_width: int = 130,
) -> tuple[ttk.Treeview, ttk.Frame]:
    """Treeview estilizado con scrollbar vertical y borde limpio."""
    outer = tk.Frame(parent, bg=Colors.BORDER, padx=1, pady=1)
    wrapper = ttk.Frame(outer, style="Card.TFrame")
    wrapper.pack(fill=tk.BOTH, expand=True)
    wrapper.grid_rowconfigure(0, weight=1)
    wrapper.grid_columnconfigure(0, weight=1)

    tree = ttk.Treeview(
        wrapper,
        columns=columns,
        show="headings",
        height=height,
        style="Modern.Treeview",
    )
    for col in columns:
        tree.heading(col, text=(headings or {}).get(col, col.capitalize()))
        tree.column(col, width=col_width, minwidth=80, stretch=True)

    vsb = ttk.Scrollbar(wrapper, orient=tk.VERTICAL, command=tree.yview, style="Modern.Vertical.TScrollbar")
    tree.configure(yscrollcommand=vsb.set)

    tree.grid(row=0, column=0, sticky="nsew")
    vsb.grid(row=0, column=1, sticky="ns")

    tree.tag_configure("odd", background=Colors.WHITE)
    tree.tag_configure("even", background=Colors.BG_APP)

    return tree, outer


def insertar_filas(tree: ttk.Treeview, filas: list[tuple]) -> None:
    """Inserta filas con alternancia sutil de color."""
    for i, valores in enumerate(filas):
        tag = "even" if i % 2 else "odd"
        tree.insert("", tk.END, values=valores, tags=(tag,))


def button_row(parent: tk.Widget, botones: list[tuple[str, Callable, str]]) -> ttk.Frame:
    """
    Fila de botones.
    botones: [(texto, comando, estilo)] — estilo: primary | secondary | danger
    """
    estilos = {"primary": "Primary.TButton", "secondary": "Secondary.TButton", "danger": "Danger.TButton"}
    frame = ttk.Frame(parent, style="Card.TFrame")
    for i, (texto, cmd, tipo) in enumerate(botones):
        ttk.Button(frame, text=texto, command=cmd, style=estilos.get(tipo, "Secondary.TButton")).pack(
            side=tk.LEFT, padx=(0 if i == 0 else SPACE_SM, 0)
        )
    return frame


class WinControlButton(tk.Frame):
    """Botón de control de ventana dibujado en canvas (nítido en Windows)."""

    def __init__(self, parent: tk.Widget, accion: str, command: Callable[[], None]) -> None:
        super().__init__(parent, bg=Colors.WHITE)
        self._accion = accion
        self._canvas = tk.Canvas(
            self, width=40, height=30, bg=Colors.WHITE, highlightthickness=0, cursor="hand2"
        )
        self._canvas.pack()
        self._redibujar(False)
        self._canvas.bind("<Button-1>", lambda _e: command())
        self._canvas.bind("<Enter>", lambda _e: self._redibujar(True))
        self._canvas.bind("<Leave>", lambda _e: self._redibujar(False))

    def _redibujar(self, activo: bool) -> None:
        dibujar_boton_ventana(self._canvas, self._accion, activo=activo)


class TopBar(tk.Frame):
    """Barra superior del dashboard — logo, título, usuario, fecha."""

    _ALTURA = 72

    def __init__(
        self,
        parent: tk.Widget,
        titulo: str,
        usuario: str,
        rol: str,
        on_logout: Callable[[], None],
        root: tk.Tk | None = None,
    ) -> None:
        super().__init__(
            parent,
            bg=Colors.WHITE,
            height=self._ALTURA,
            highlightbackground=Colors.BORDER_SOFT,
            highlightthickness=1,
        )
        self.grid_propagate(False)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        logo_wrap = tk.Frame(self, bg=Colors.WHITE)
        logo_wrap.grid(row=0, column=0, padx=(SPACE_LG, SPACE_SM), pady=0, sticky="ns")
        logo = tk.Canvas(logo_wrap, width=44, height=44, bg=Colors.WHITE, highlightthickness=0)
        logo.pack(expand=True)
        dibujar_logo(logo, 44, bg=Colors.WHITE)

        info = ttk.Frame(self, style="TopBar.TFrame")
        info.grid(row=0, column=1, sticky="w")
        ttk.Label(info, text=titulo, style="TopBarTitle.TLabel").pack(anchor=tk.W)
        ttk.Label(info, text=SUBTITULO_INSTITUCION, style="TopBarUser.TLabel").pack(anchor=tk.W, pady=(2, 0))

        derecha = ttk.Frame(self, style="TopBar.TFrame")
        derecha.grid(row=0, column=2, sticky="e", padx=SPACE_LG)

        user_box = tk.Frame(derecha, bg=Colors.BG_APP, highlightbackground=Colors.BORDER, highlightthickness=1)
        user_box.pack(side=tk.LEFT, padx=(0, SPACE_MD))
        inner = ttk.Frame(user_box, style="Card.TFrame", padding=(SPACE_MD, SPACE_SM))
        inner.pack()
        ttk.Label(inner, text=usuario, style="Card.TLabel", font=(FONT, 11, "bold")).pack(anchor=tk.E)
        ttk.Label(inner, text=rol.capitalize(), style="Field.TLabel").pack(anchor=tk.E)

        fecha = datetime.now().strftime("%d/%m/%Y")
        ttk.Label(derecha, text=fecha, style="TopBarUser.TLabel").pack(side=tk.LEFT, padx=(0, SPACE_MD))

        if root is not None:
            win_btns = tk.Frame(derecha, bg=Colors.WHITE)
            win_btns.pack(side=tk.LEFT, padx=(0, SPACE_SM))
            WinControlButton(win_btns, "minimizar", root.iconify).pack(side=tk.LEFT)
            WinControlButton(win_btns, "maximizar", lambda: None).pack(side=tk.LEFT)
            WinControlButton(win_btns, "cerrar", root.destroy).pack(side=tk.LEFT)

        ttk.Button(derecha, text="Cerrar sesión", style="Danger.TButton", command=on_logout).pack(side=tk.LEFT)


class NavItem(tk.Frame):
    """Botón de navegación lateral — tarjeta con icono vectorial, texto e indicador."""

    def __init__(
        self,
        parent: tk.Widget,
        texto: str,
        command: Callable[[], None],
        *,
        icono: str | None = None,
    ) -> None:
        super().__init__(parent, bg=Colors.WHITE, cursor="hand2")
        self._command = command
        self._seleccionado = False
        self._texto = texto
        self._tipo = _tipo_nav(texto, icono)

        self._indicador = tk.Frame(self, bg=Colors.WHITE, width=4)
        self._indicador.pack(side=tk.LEFT, fill=tk.Y)

        self._cuerpo = tk.Frame(self, bg=Colors.WHITE, highlightbackground=Colors.BORDER, highlightthickness=0)
        self._cuerpo.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, SPACE_SM), pady=SPACE_XS)

        inner = tk.Frame(self._cuerpo, bg=Colors.WHITE)
        inner.pack(fill=tk.X, padx=SPACE_MD, pady=SPACE_SM)

        self._badge = tk.Canvas(inner, width=38, height=38, bg=Colors.WHITE, highlightthickness=0)
        self._badge.pack(side=tk.LEFT)
        self._redibujar_icono()

        self._label = tk.Label(
            inner,
            text=texto,
            bg=Colors.WHITE,
            fg=Colors.TEXT_PRIMARY,
            font=(FONT, 11),
            anchor="w",
        )
        self._label.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(SPACE_SM, 0))

        for w in (self, self._cuerpo, inner, self._label, self._badge):
            w.bind("<Button-1>", self._click)
            w.bind("<Enter>", self._hover_enter)
            w.bind("<Leave>", self._hover_leave)

    def _redibujar_icono(self) -> None:
        if self._seleccionado:
            dibujar_icono_nav(
                self._badge, self._tipo, fg=Colors.WHITE, bg=Colors.PRIMARY, borde=Colors.PRIMARY
            )
        else:
            dibujar_icono_nav(self._badge, self._tipo)

    def _click(self, _=None) -> None:
        self._command()

    def _hover_enter(self, _=None) -> None:
        if not self._seleccionado:
            self._cuerpo.configure(bg=Colors.BG_APP, highlightthickness=1, highlightbackground=Colors.BORDER)
            self._label.configure(bg=Colors.BG_APP)
            self._badge.configure(bg=Colors.BG_APP)

    def _hover_leave(self, _=None) -> None:
        if not self._seleccionado:
            self._restaurar_normal()

    def _restaurar_normal(self) -> None:
        self._cuerpo.configure(bg=Colors.WHITE, highlightthickness=0)
        self._label.configure(bg=Colors.WHITE)
        self._badge.configure(bg=Colors.WHITE)
        self._redibujar_icono()

    def seleccionar(self) -> None:
        self._seleccionado = True
        self._indicador.configure(bg=Colors.PRIMARY)
        self._cuerpo.configure(bg=Colors.PRIMARY_LIGHT, highlightthickness=1, highlightbackground=Colors.PRIMARY_SOFT)
        self._label.configure(bg=Colors.PRIMARY_LIGHT, fg=Colors.PRIMARY, font=(FONT, 11, "bold"))
        self._badge.configure(bg=Colors.PRIMARY_LIGHT)
        self._redibujar_icono()

    def deseleccionar(self) -> None:
        self._seleccionado = False
        self._indicador.configure(bg=Colors.WHITE)
        self._restaurar_normal()
        self._label.configure(fg=Colors.TEXT_PRIMARY, font=(FONT, 11))


class Sidebar(tk.Frame):
    """Menú lateral con navegación tipo tarjetas."""

    def __init__(self, parent: tk.Widget, titulo: str = "Menú") -> None:
        super().__init__(
            parent,
            bg=Colors.WHITE,
            width=260,
            highlightbackground=Colors.BORDER,
            highlightthickness=1,
        )
        self.grid_propagate(False)
        self._items: list[NavItem] = []

        header = tk.Frame(self, bg=Colors.WHITE)
        header.pack(fill=tk.X, padx=SPACE_LG, pady=(SPACE_LG, SPACE_MD))
        tk.Label(header, text=titulo, bg=Colors.WHITE, fg=Colors.TEXT_MUTED, font=(FONT, 10, "bold")).pack(anchor=tk.W)

        self._nav = tk.Frame(self, bg=Colors.WHITE)
        self._nav.pack(fill=tk.BOTH, expand=True, padx=SPACE_SM, pady=(0, SPACE_LG))

    def agregar_item(self, texto: str, command: Callable[[], None], *, icono: str | None = None) -> NavItem:
        item = NavItem(self._nav, texto, command, icono=icono)
        item.pack(fill=tk.X, pady=SPACE_XS)
        self._items.append(item)
        return item

    def marcar(self, indice: int) -> None:
        for i, item in enumerate(self._items):
            if i == indice:
                item.seleccionar()
            else:
                item.deseleccionar()
