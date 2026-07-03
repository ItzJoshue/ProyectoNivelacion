import tkinter as tk
from tkinter import ttk

from servicios.autenticacion_servicio import AutenticacionServicio
from servicios.matricula_servicio import MatriculaServicio
from Vistas.ui.components import Card, page_header, styled_text


class MiPerfilFrame(ttk.Frame):
    """Vista restringida: el estudiante solo ve su propio perfil."""

    def __init__(
        self,
        parent: tk.Widget,
        cedula: str,
        auth: AutenticacionServicio,
        matricula: MatriculaServicio,
    ) -> None:
        super().__init__(parent, style="Content.TFrame")
        self.cedula = cedula
        self.auth = auth
        self.matricula = matricula

        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        page_header(self, "Mi perfil", "Información académica de su cuenta").grid(row=0, column=0, sticky="ew")

        card = Card(self, title="Datos personales")
        card.grid(row=1, column=0, sticky="nsew")
        card.body.rowconfigure(0, weight=1)
        card.body.columnconfigure(0, weight=1)

        self.texto = styled_text(card.body, height=16, wrap=tk.WORD)
        self.texto.grid(row=0, column=0, sticky="nsew")
        self.refrescar()

    def refrescar(self) -> None:
        self.texto.config(state=tk.NORMAL)
        self.texto.delete("1.0", tk.END)
        estudiante = self.auth.obtener_perfil_estudiante(self.cedula)
        if estudiante is None:
            self.texto.insert(tk.END, "No se encontró su perfil académico.")
        else:
            self.texto.insert(tk.END, f"{estudiante.obtener_resumen()}\n\n")
            self.texto.insert(tk.END, f"Carrera: {estudiante.carrera}\n")
            self.texto.insert(tk.END, f"Email: {estudiante.email}\n")
            self.texto.insert(tk.END, f"Materias: {', '.join(estudiante.materias) or 'Ninguna'}\n")
            mats = self.matricula.matriculas_de_estudiante(self.cedula)
            self.texto.insert(tk.END, f"\nMatrículas activas: {len(mats)}\n")
        self.texto.config(state=tk.DISABLED)
