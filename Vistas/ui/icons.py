"""Iconografía vectorial en canvas — nítida en cualquier resolución."""

from __future__ import annotations

import tkinter as tk

from Vistas.ui.colors import Colors
from Vistas.ui.theme import FONT

ICONOS_NAV: dict[str, str] = {
    "estudiantes": "estudiantes",
    "materias": "materias",
    "calificaciones": "calificaciones",
    "aulas": "aulas",
    "cursos": "cursos",
    "postulantes": "postulantes",
    "matrículas": "matriculas",
    "matriculas": "matriculas",
    "reportes": "reportes",
    "mi perfil": "perfil",
    "mis calificaciones": "notas",
}


def _tipo_nav(texto: str, icono: str | None = None) -> str:
    if icono:
        return icono
    return ICONOS_NAV.get(texto.lower(), "default")


def dibujar_logo(canvas: tk.Canvas, size: int, *, bg: str | None = None) -> None:
    """Logo institucional circular con tipografía centrada."""
    canvas.delete("all")
    fondo = bg or canvas.cget("bg")
    m = max(2, size // 14)
    canvas.create_oval(m, m, size - m, size - m, fill=Colors.PRIMARY, outline=Colors.PRIMARY_SOFT, width=1)
    canvas.create_text(
        size // 2,
        size // 2 + 1,
        text="U",
        fill=Colors.WHITE,
        font=(FONT, max(10, size // 3), "bold"),
    )


def dibujar_icono_nav(
    canvas: tk.Canvas,
    tipo: str,
    *,
    size: int = 36,
    fg: str = Colors.PRIMARY,
    bg: str = Colors.PRIMARY_LIGHT,
    borde: str = Colors.BORDER,
) -> None:
    """Dibuja pictogramas simples para el menú lateral."""
    canvas.delete("all")
    m = 2
    canvas.create_oval(m, m, size - m, size - m, fill=bg, outline=borde, width=1)
    cx, cy = size // 2, size // 2

    if tipo == "estudiantes" or tipo == "perfil" or tipo == "postulantes":
        canvas.create_oval(cx - 4, cy - 9, cx + 4, cy - 1, fill=fg, outline="")
        canvas.create_arc(cx - 7, cy - 1, cx + 7, cy + 11, start=200, extent=140, style=tk.PIESLICE, fill=fg, outline="")
    elif tipo == "materias" or tipo == "cursos":
        canvas.create_rectangle(cx - 8, cy - 7, cx + 8, cy + 8, fill=fg, outline="")
        canvas.create_line(cx - 6, cy - 3, cx + 6, cy - 3, fill=bg, width=2)
        canvas.create_line(cx - 6, cy + 1, cx + 4, cy + 1, fill=bg, width=2)
    elif tipo == "calificaciones" or tipo == "notas":
        for i, h in enumerate((6, 10, 4, 8)):
            x = cx - 9 + i * 5
            canvas.create_rectangle(x, cy + 5 - h, x + 3, cy + 5, fill=fg, outline="")
    elif tipo == "aulas":
        canvas.create_rectangle(cx - 9, cy - 5, cx + 9, cy + 8, fill=fg, outline="")
        canvas.create_rectangle(cx - 3, cy + 1, cx + 3, cy + 8, fill=bg, outline="")
    elif tipo == "matriculas":
        canvas.create_oval(cx - 8, cy - 2, cx - 1, cy + 5, fill=fg, outline="")
        canvas.create_oval(cx + 1, cy - 2, cx + 8, cy + 5, fill=fg, outline="")
        canvas.create_line(cx - 4, cy + 1, cx + 4, cy + 1, fill=bg, width=2)
    elif tipo == "reportes":
        canvas.create_rectangle(cx - 7, cy - 8, cx + 7, cy + 8, fill=fg, outline="")
        canvas.create_line(cx - 4, cy - 4, cx + 4, cy - 4, fill=bg, width=2)
        canvas.create_line(cx - 4, cy, cx + 2, cy, fill=bg, width=2)
        canvas.create_line(cx - 4, cy + 4, cx + 4, cy + 4, fill=bg, width=2)
    else:
        canvas.create_oval(cx - 5, cy - 5, cx + 5, cy + 5, fill=fg, outline="")


def dibujar_boton_ventana(canvas: tk.Canvas, accion: str, *, activo: bool = False) -> None:
    """Controles de ventana dibujados (minimizar, maximizar, cerrar)."""
    canvas.delete("all")
    w = int(canvas.cget("width"))
    h = int(canvas.cget("height"))
    fondo = Colors.DANGER_LIGHT if accion == "cerrar" and activo else (Colors.BG_APP if activo else Colors.WHITE)
    canvas.configure(bg=fondo)

    color = Colors.DANGER if accion == "cerrar" else Colors.TEXT_SECONDARY
    cx, cy = w // 2, h // 2

    if accion == "minimizar":
        canvas.create_line(7, cy + 1, w - 7, cy + 1, fill=color, width=2, capstyle=tk.ROUND)
    elif accion == "maximizar":
        canvas.create_rectangle(7, 7, w - 7, h - 7, outline=color, width=1.5)
    elif accion == "cerrar":
        canvas.create_line(8, 8, w - 8, h - 8, fill=color, width=2, capstyle=tk.ROUND)
        canvas.create_line(w - 8, 8, 8, h - 8, fill=color, width=2, capstyle=tk.ROUND)
