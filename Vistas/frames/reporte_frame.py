import tkinter as tk
from tkinter import messagebox, ttk

from infraestructura.utilidades.almacenamiento import DATA_DIR
from servicios.matricula_servicio import MatriculaServicio
from Vistas.ui.components import Card, SPACE_MD, button_row, page_header, styled_text


class ReporteFrame(ttk.Frame):
    def __init__(self, parent: tk.Widget, matricula: MatriculaServicio) -> None:
        super().__init__(parent, style="Content.TFrame")
        self.matricula = matricula

        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)

        page_header(self, "Reportes", "Genere y consulte reportes del sistema").grid(row=0, column=0, sticky="ew")

        acciones_card = Card(self, title="Acciones")
        acciones_card.grid(row=1, column=0, sticky="ew", pady=(0, SPACE_MD))
        button_row(
            acciones_card.body,
            [
                ("Generar reporte", self._generar, "primary"),
                ("Ver carpeta de datos", self._ruta, "secondary"),
            ],
        ).pack(anchor=tk.W)

        preview_card = Card(self, title="Vista previa del reporte")
        preview_card.grid(row=2, column=0, sticky="nsew")
        preview_card.body.rowconfigure(0, weight=1)
        preview_card.body.columnconfigure(0, weight=1)

        self.texto = styled_text(preview_card.body, height=22, wrap=tk.WORD)
        self.texto.grid(row=0, column=0, sticky="nsew")

    def _generar(self) -> None:
        self.texto.delete("1.0", tk.END)
        self.texto.insert(tk.END, self.matricula.generar_reporte())

    def _ruta(self) -> None:
        messagebox.showinfo("Datos", f"Los archivos JSON están en:\n{DATA_DIR}")
