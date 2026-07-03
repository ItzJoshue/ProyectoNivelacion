import tkinter as tk
from tkinter import ttk

from servicios.autenticacion_servicio import AutenticacionServicio
from servicios.gestor_academico import GestorAcademico
from servicios.matricula_servicio import MatriculaServicio


class MiPerfilFrame(ttk.Frame):
    """Vista restringida: el estudiante solo ve su propio perfil."""

    def __init__(self, parent: tk.Widget, cedula: str, auth: AutenticacionServicio, matricula: MatriculaServicio) -> None:
        super().__init__(parent, padding=16)
        self.cedula = cedula
        self.auth = auth
        self.matricula = matricula
        self.texto = tk.Text(self, height=16, wrap=tk.WORD, font=("Segoe UI", 10))
        self.texto.pack(fill=tk.BOTH, expand=True)
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
