"""Configuración global de ttk.Style — lenguaje visual unificado."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from Vistas.ui.colors import Colors

FONT = "Segoe UI"
FONT_FALLBACK = "Arial"


def _font(size: int, weight: str = "normal") -> tuple:
    return (FONT, size, weight) if weight != "normal" else (FONT, size)


def aplicar_tema(root: tk.Misc) -> ttk.Style:
    """Aplica el tema institucional a toda la aplicación."""
    root.configure(bg=Colors.GRAY_50)

    style = ttk.Style(root)
    try:
        style.theme_use("clam")
    except tk.TclError:
        pass

    # ── Frames ──────────────────────────────────────────────────────────
    style.configure("App.TFrame", background=Colors.GRAY_50)
    style.configure("Card.TFrame", background=Colors.WHITE)
    style.configure("Sidebar.TFrame", background=Colors.WHITE)
    style.configure("TopBar.TFrame", background=Colors.WHITE)
    style.configure("Content.TFrame", background=Colors.GRAY_50)

    # ── Labels ──────────────────────────────────────────────────────────
    style.configure("TLabel", background=Colors.GRAY_50, foreground=Colors.GRAY_800, font=_font(10))
    style.configure("Card.TLabel", background=Colors.WHITE, foreground=Colors.GRAY_800, font=_font(10))
    style.configure("Sidebar.TLabel", background=Colors.WHITE, foreground=Colors.GRAY_800, font=_font(10))
    style.configure("TopBar.TLabel", background=Colors.WHITE, foreground=Colors.GRAY_800, font=_font(10))
    style.configure("Title.TLabel", font=_font(22, "bold"), foreground=Colors.GRAY_800)
    style.configure("Subtitle.TLabel", font=_font(13), foreground=Colors.GRAY_600)
    style.configure("PageTitle.TLabel", font=_font(18, "bold"), foreground=Colors.GRAY_800, background=Colors.GRAY_50)
    style.configure("CardTitle.TLabel", font=_font(14, "bold"), foreground=Colors.GRAY_800, background=Colors.WHITE)
    style.configure("Field.TLabel", font=_font(9), foreground=Colors.GRAY_600, background=Colors.WHITE)
    style.configure("Muted.TLabel", font=_font(9), foreground=Colors.GRAY_600, background=Colors.GRAY_50)
    style.configure("TopBarTitle.TLabel", font=_font(13, "bold"), foreground=Colors.GRAY_800, background=Colors.WHITE)
    style.configure("TopBarUser.TLabel", font=_font(10), foreground=Colors.GRAY_600, background=Colors.WHITE)

    # ── Botones ─────────────────────────────────────────────────────────
    _btn_base = dict(focuscolor=Colors.WHITE, borderwidth=0, padding=(20, 10), font=_font(10))

    style.configure(
        "Primary.TButton",
        background=Colors.GREEN,
        foreground=Colors.WHITE,
        **_btn_base,
    )
    style.map(
        "Primary.TButton",
        background=[("active", Colors.GREEN_HOVER), ("disabled", Colors.GRAY_100)],
        foreground=[("disabled", Colors.GRAY_600)],
    )

    style.configure(
        "Secondary.TButton",
        background=Colors.WHITE,
        foreground=Colors.GRAY_800,
        borderwidth=1,
        relief="solid",
        padding=(18, 9),
        font=_font(10),
    )
    style.map(
        "Secondary.TButton",
        background=[("active", Colors.GRAY_50), ("disabled", Colors.GRAY_100)],
        foreground=[("disabled", Colors.GRAY_600)],
        bordercolor=[("active", Colors.GRAY_600), ("!active", Colors.GRAY_300)],
    )

    style.configure(
        "Danger.TButton",
        background=Colors.RED,
        foreground=Colors.WHITE,
        **_btn_base,
    )
    style.map(
        "Danger.TButton",
        background=[("active", Colors.RED_HOVER), ("disabled", Colors.GRAY_100)],
        foreground=[("disabled", Colors.GRAY_600)],
    )

    style.configure(
        "Ghost.TButton",
        background=Colors.WHITE,
        foreground=Colors.GRAY_600,
        borderwidth=0,
        padding=(12, 8),
        font=_font(10),
    )
    style.map(
        "Ghost.TButton",
        background=[("active", Colors.GRAY_50)],
        foreground=[("active", Colors.GRAY_800)],
    )

    style.configure(
        "Nav.TButton",
        background=Colors.WHITE,
        foreground=Colors.GRAY_800,
        borderwidth=0,
        anchor="w",
        padding=(16, 14),
        font=_font(10),
    )
    style.map(
        "Nav.TButton",
        background=[("active", Colors.GRAY_50)],
    )

    # ── Entradas ────────────────────────────────────────────────────────
    style.configure(
        "Modern.TEntry",
        fieldbackground=Colors.WHITE,
        foreground=Colors.GRAY_800,
        bordercolor=Colors.GRAY_300,
        lightcolor=Colors.GRAY_300,
        darkcolor=Colors.GRAY_300,
        padding=(10, 8),
        font=_font(10),
    )
    style.map(
        "Modern.TEntry",
        bordercolor=[("focus", Colors.GREEN), ("!focus", Colors.GRAY_300)],
        lightcolor=[("focus", Colors.GREEN)],
    )

    style.configure(
        "Modern.TCombobox",
        fieldbackground=Colors.WHITE,
        foreground=Colors.GRAY_800,
        bordercolor=Colors.GRAY_300,
        arrowcolor=Colors.GRAY_600,
        padding=(8, 8),
        font=_font(10),
    )
    style.map(
        "Modern.TCombobox",
        bordercolor=[("focus", Colors.GREEN), ("!focus", Colors.GRAY_300)],
        fieldbackground=[("readonly", Colors.WHITE)],
    )

    # ── Treeview ────────────────────────────────────────────────────────
    style.configure(
        "Modern.Treeview",
        background=Colors.WHITE,
        foreground=Colors.GRAY_800,
        fieldbackground=Colors.WHITE,
        borderwidth=0,
        rowheight=36,
        font=_font(10),
    )
    style.configure(
        "Modern.Treeview.Heading",
        background=Colors.GREEN,
        foreground=Colors.WHITE,
        borderwidth=0,
        relief="flat",
        padding=(12, 10),
        font=_font(10, "bold"),
    )
    style.map(
        "Modern.Treeview",
        background=[("selected", Colors.RED)],
        foreground=[("selected", Colors.WHITE)],
    )
    style.map(
        "Modern.Treeview.Heading",
        background=[("active", Colors.GREEN_HOVER)],
    )

    # ── Notebook ────────────────────────────────────────────────────────
    style.configure("Modern.TNotebook", background=Colors.GRAY_50, borderwidth=0, tabmargins=(0, 0, 0, 0))
    style.configure(
        "Modern.TNotebook.Tab",
        background=Colors.GRAY_100,
        foreground=Colors.GRAY_600,
        padding=(20, 10),
        font=_font(10),
    )
    style.map(
        "Modern.TNotebook.Tab",
        background=[("selected", Colors.WHITE), ("active", Colors.GRAY_50)],
        foreground=[("selected", Colors.GREEN), ("active", Colors.GRAY_800)],
    )

    # ── Scrollbar ───────────────────────────────────────────────────────
    style.configure(
        "Modern.Vertical.TScrollbar",
        background=Colors.GRAY_100,
        troughcolor=Colors.GRAY_50,
        borderwidth=0,
        arrowsize=14,
        width=10,
    )
    style.map(
        "Modern.Vertical.TScrollbar",
        background=[("active", Colors.GRAY_300), ("!active", Colors.GRAY_100)],
    )
    style.configure(
        "Modern.Horizontal.TScrollbar",
        background=Colors.GRAY_100,
        troughcolor=Colors.GRAY_50,
        borderwidth=0,
        arrowsize=14,
        width=10,
    )
    style.map(
        "Modern.Horizontal.TScrollbar",
        background=[("active", Colors.GRAY_300), ("!active", Colors.GRAY_100)],
    )

    # ── Progressbar ─────────────────────────────────────────────────────
    style.configure(
        "Modern.Horizontal.TProgressbar",
        background=Colors.GREEN,
        troughcolor=Colors.GRAY_100,
        borderwidth=0,
        thickness=8,
    )

    # ── Check / Radio ───────────────────────────────────────────────────
    style.configure(
        "Modern.TRadiobutton",
        background=Colors.WHITE,
        foreground=Colors.GRAY_800,
        font=_font(10),
        padding=(4, 4),
    )
    style.map(
        "Modern.TRadiobutton",
        background=[("active", Colors.WHITE)],
        indicatorcolor=[("selected", Colors.GREEN), ("!selected", Colors.GRAY_300)],
    )

    style.configure(
        "Modern.TCheckbutton",
        background=Colors.WHITE,
        foreground=Colors.GRAY_800,
        font=_font(10),
        padding=(4, 4),
    )
    style.map(
        "Modern.TCheckbutton",
        background=[("active", Colors.WHITE)],
        indicatorcolor=[("selected", Colors.GREEN), ("!selected", Colors.GRAY_300)],
    )

    # ── LabelFrame (legacy fallback) ────────────────────────────────────
    style.configure(
        "Card.TLabelframe",
        background=Colors.WHITE,
        bordercolor=Colors.GRAY_300,
        relief="solid",
        borderwidth=1,
    )
    style.configure(
        "Card.TLabelframe.Label",
        background=Colors.WHITE,
        foreground=Colors.GRAY_800,
        font=_font(11, "bold"),
    )

    return style
