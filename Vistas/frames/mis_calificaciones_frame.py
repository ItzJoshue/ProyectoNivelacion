import tkinter as tk
from tkinter import ttk

from servicios.autenticacion_servicio import AutenticacionServicio
from servicios.matricula_servicio import MatriculaServicio


class MisCalificacionesFrame(ttk.Frame):
    """Vista restringida: solo las calificaciones del estudiante autenticado."""

    def __init__(self, parent: tk.Widget, cedula: str, auth: AutenticacionServicio, matricula: MatriculaServicio) -> None:
        super().__init__(parent, padding=16)
        self.cedula = cedula
        self.auth = auth
        self.matricula = matricula
        ttk.Label(self, text="Mis calificaciones", font=("Segoe UI", 14, "bold")).pack(anchor=tk.W, pady=(0, 10))
        self.tabla = ttk.Treeview(self, columns=("materia", "nota"), show="headings", height=10)
        self.tabla.heading("materia", text="Materia")
        self.tabla.heading("nota", text="Nota")
        self.tabla.pack(fill=tk.X, pady=(0, 12))
        self.texto = tk.Text(self, height=10, wrap=tk.WORD)
        self.texto.pack(fill=tk.BOTH, expand=True)
        self.refrescar()

    def refrescar(self) -> None:
        for i in self.tabla.get_children():
            self.tabla.delete(i)
        self.texto.config(state=tk.NORMAL)
        self.texto.delete("1.0", tk.END)

        estudiante = self.auth.obtener_perfil_estudiante(self.cedula)
        if estudiante is None:
            self.texto.insert(tk.END, "Sin datos académicos.")
        else:
            for materia, nota in estudiante.calificaciones.items():
                self.tabla.insert("", tk.END, values=(materia, nota))
            self.texto.insert(tk.END, f"Promedio general: {estudiante.promedio}\n\n")
            cursos = {c.id: c.nombre for c in self.matricula.listar_cursos()}
            for m in self.matricula.matriculas_de_estudiante(self.cedula):
                self.texto.insert(tk.END, f"Curso matriculado: {cursos.get(m.id_curso, m.id_curso)}\n")
        self.texto.config(state=tk.DISABLED)
