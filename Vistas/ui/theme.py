"""Configuración global de ttk.Style — lenguaje visual unificado."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from Vistas.ui.colors import Colors

FONT = "Segoe UI"
FONT_FALLBACK = "Arial"

TITULO_APP = "Sistema de Nivelación ULEAM"
SUBTITULO_INSTITUCION = "Universidad Laica Eloy Alfaro de Manabí"


def _font(size: int, weight: str = "normal") -> tuple:
    return (FONT, size, weight) if weight != "normal" else (FONT, size)


def aplicar_tema(root: tk.Misc) -> ttk.Style:
    """Aplica el tema suave y moderno a toda la aplicación."""
    root.configure(bg=Colors.BG_APP)

    style = ttk.Style(root)
    try:
        style.theme_use("clam")
    except tk.TclError:
        pass

    # ── Frames ──────────────────────────────────────────────────────────
    style.configure("App.TFrame", background=Colors.BG_APP)
    style.configure("Card.TFrame", background=Colors.WHITE)
    style.configure("Sidebar.TFrame", background=Colors.WHITE)
    style.configure("TopBar.TFrame", background=Colors.WHITE)
    style.configure("Content.TFrame", background=Colors.BG_APP)

    # ── Labels ──────────────────────────────────────────────────────────
    style.configure("TLabel", background=Colors.BG_APP, foreground=Colors.TEXT_PRIMARY, font=_font(11))
    style.configure("Card.TLabel", background=Colors.WHITE, foreground=Colors.TEXT_PRIMARY, font=_font(11))
    style.configure("Sidebar.TLabel", background=Colors.WHITE, foreground=Colors.TEXT_PRIMARY, font=_font(11))
    style.configure("TopBar.TLabel", background=Colors.WHITE, foreground=Colors.TEXT_PRIMARY, font=_font(11))
    style.configure("Title.TLabel", font=_font(24, "bold"), foreground=Colors.TEXT_PRIMARY)
    style.configure("Subtitle.TLabel", font=_font(12), foreground=Colors.TEXT_SECONDARY)
    style.configure(
        "PageTitle.TLabel",
        font=_font(20, "bold"),
        foreground=Colors.TEXT_PRIMARY,
        background=Colors.BG_APP,
    )
    style.configure(
        "CardTitle.TLabel",
        font=_font(13, "bold"),
        foreground=Colors.TEXT_PRIMARY,
        background=Colors.WHITE,
    )
    style.configure("Field.TLabel", font=_font(10), foreground=Colors.TEXT_SECONDARY, background=Colors.WHITE)
    style.configure("Muted.TLabel", font=_font(11), foreground=Colors.TEXT_MUTED, background=Colors.BG_APP)
    style.configure(
        "TopBarTitle.TLabel",
        font=_font(14, "bold"),
        foreground=Colors.TEXT_PRIMARY,
        background=Colors.WHITE,
    )
    style.configure(
        "TopBarUser.TLabel",
        font=_font(10),
        foreground=Colors.TEXT_SECONDARY,
        background=Colors.WHITE,
    )

    # ── Botones ─────────────────────────────────────────────────────────
    _btn_base = dict(focuscolor=Colors.WHITE, borderwidth=0, padding=(22, 11), font=_font(11))

    style.configure(
        "Primary.TButton",
        background=Colors.PRIMARY,
        foreground=Colors.WHITE,
        **_btn_base,
    )
    style.map(
        "Primary.TButton",
        background=[("active", Colors.PRIMARY_HOVER), ("disabled", Colors.BG_SUBTLE)],
        foreground=[("disabled", Colors.TEXT_MUTED)],
    )

    style.configure(
        "Secondary.TButton",
        background=Colors.WHITE,
        foreground=Colors.TEXT_PRIMARY,
        borderwidth=1,
        relief="solid",
        padding=(20, 10),
        font=_font(11),
    )
    style.map(
        "Secondary.TButton",
        background=[("active", Colors.BG_APP), ("disabled", Colors.BG_SUBTLE)],
        foreground=[("disabled", Colors.TEXT_MUTED)],
        bordercolor=[("active", Colors.BORDER_FOCUS), ("!active", Colors.BORDER)],
    )

    style.configure(
        "Danger.TButton",
        background=Colors.DANGER,
        foreground=Colors.WHITE,
        **_btn_base,
    )
    style.map(
        "Danger.TButton",
        background=[("active", Colors.DANGER_HOVER), ("disabled", Colors.BG_SUBTLE)],
        foreground=[("disabled", Colors.TEXT_MUTED)],
    )

    style.configure(
        "Ghost.TButton",
        background=Colors.WHITE,
        foreground=Colors.TEXT_SECONDARY,
        borderwidth=0,
        padding=(12, 8),
        font=_font(10),
    )
    style.map(
        "Ghost.TButton",
        background=[("active", Colors.BG_APP)],
        foreground=[("active", Colors.TEXT_PRIMARY)],
    )

    style.configure(
        "Nav.TButton",
        background=Colors.WHITE,
        foreground=Colors.TEXT_PRIMARY,
        borderwidth=0,
        anchor="w",
        padding=(16, 14),
        font=_font(10),
    )
    style.map(
        "Nav.TButton",
        background=[("active", Colors.BG_APP)],
    )

    # ── Entradas ────────────────────────────────────────────────────────
    style.configure(
        "Modern.TEntry",
        fieldbackground=Colors.WHITE,
        foreground=Colors.TEXT_PRIMARY,
        bordercolor=Colors.BORDER,
        lightcolor=Colors.BORDER,
        darkcolor=Colors.BORDER,
        padding=(10, 9),
        font=_font(11),
    )
    style.map(
        "Modern.TEntry",
        bordercolor=[("focus", Colors.BORDER_FOCUS), ("!focus", Colors.BORDER)],
        lightcolor=[("focus", Colors.BORDER_FOCUS)],
    )

    style.configure(
        "Modern.TCombobox",
        fieldbackground=Colors.WHITE,
        foreground=Colors.TEXT_PRIMARY,
        bordercolor=Colors.BORDER,
        arrowcolor=Colors.TEXT_SECONDARY,
        padding=(10, 9),
        font=_font(11),
    )
    style.map(
        "Modern.TCombobox",
        bordercolor=[("focus", Colors.BORDER_FOCUS), ("!focus", Colors.BORDER)],
        fieldbackground=[("readonly", Colors.WHITE)],
    )

    # ── Treeview ────────────────────────────────────────────────────────
    style.configure(
        "Modern.Treeview",
        background=Colors.WHITE,
        foreground=Colors.TEXT_PRIMARY,
        fieldbackground=Colors.WHITE,
        borderwidth=0,
        rowheight=40,
        font=_font(11),
    )
    style.configure(
        "Modern.Treeview.Heading",
        background=Colors.PRIMARY,
        foreground=Colors.WHITE,
        borderwidth=0,
        relief="flat",
        padding=(14, 11),
        font=_font(11, "bold"),
    )
    style.map(
        "Modern.Treeview",
        background=[("selected", Colors.PRIMARY_SOFT)],
        foreground=[("selected", Colors.TEXT_PRIMARY)],
    )
    style.map(
        "Modern.Treeview.Heading",
        background=[("active", Colors.PRIMARY_HOVER)],
    )

    # ── Notebook ────────────────────────────────────────────────────────
    style.configure("Modern.TNotebook", background=Colors.BG_APP, borderwidth=0, tabmargins=(0, 0, 0, 0))
    style.configure(
        "Modern.TNotebook.Tab",
        background=Colors.BG_SUBTLE,
        foreground=Colors.TEXT_SECONDARY,
        padding=(20, 10),
        font=_font(10),
    )
    style.map(
        "Modern.TNotebook.Tab",
        background=[("selected", Colors.WHITE), ("active", Colors.BG_APP)],
        foreground=[("selected", Colors.PRIMARY), ("active", Colors.TEXT_PRIMARY)],
    )

    # ── Scrollbar ───────────────────────────────────────────────────────
    style.configure(
        "Modern.Vertical.TScrollbar",
        background=Colors.BG_MUTED,
        troughcolor=Colors.BG_APP,
        borderwidth=0,
        arrowsize=12,
        width=8,
    )
    style.map(
        "Modern.Vertical.TScrollbar",
        background=[("active", Colors.BORDER), ("!active", Colors.BG_MUTED)],
    )
    style.configure(
        "Modern.Horizontal.TScrollbar",
        background=Colors.BG_MUTED,
        troughcolor=Colors.BG_APP,
        borderwidth=0,
        arrowsize=12,
        width=8,
    )
    style.map(
        "Modern.Horizontal.TScrollbar",
        background=[("active", Colors.BORDER), ("!active", Colors.BG_MUTED)],
    )

    # ── Progressbar ─────────────────────────────────────────────────────
    style.configure(
        "Modern.Horizontal.TProgressbar",
        background=Colors.SUCCESS,
        troughcolor=Colors.BG_SUBTLE,
        borderwidth=0,
        thickness=8,
    )

    # ── Check / Radio ───────────────────────────────────────────────────
    style.configure(
        "Modern.TRadiobutton",
        background=Colors.WHITE,
        foreground=Colors.TEXT_PRIMARY,
        font=_font(10),
        padding=(4, 4),
    )
    style.map(
        "Modern.TRadiobutton",
        background=[("active", Colors.WHITE)],
        indicatorcolor=[("selected", Colors.PRIMARY), ("!selected", Colors.BORDER)],
    )

    style.configure(
        "Modern.TCheckbutton",
        background=Colors.WHITE,
        foreground=Colors.TEXT_PRIMARY,
        font=_font(10),
        padding=(4, 4),
    )
    style.map(
        "Modern.TCheckbutton",
        background=[("active", Colors.WHITE)],
        indicatorcolor=[("selected", Colors.PRIMARY), ("!selected", Colors.BORDER)],
    )

    # ── LabelFrame (legacy fallback) ────────────────────────────────────
    style.configure(
        "Card.TLabelframe",
        background=Colors.WHITE,
        bordercolor=Colors.BORDER,
        relief="solid",
        borderwidth=1,
    )
    style.configure(
        "Card.TLabelframe.Label",
        background=Colors.WHITE,
        foreground=Colors.TEXT_PRIMARY,
        font=_font(11, "bold"),
    )

    return style
