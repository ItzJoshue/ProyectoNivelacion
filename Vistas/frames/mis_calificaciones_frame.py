import tkinter as tk
from tkinter import ttk

from domain.entidades.estudiante import NOTA_MINIMA_APROBACION
from servicios.autenticacion_servicio import AutenticacionServicio
from servicios.gestor_academico import GestorAcademico
from servicios.matricula_servicio import MatriculaServicio
from Vistas.ui.components import Card, SPACE_MD, create_treeview, insertar_filas, page_header, styled_text


class MisCalificacionesFrame(ttk.Frame):
    """Vista restringida: solo las calificaciones del estudiante autenticado."""

    def __init__(
        self,
        parent: tk.Widget,
        cedula: str,
        auth: AutenticacionServicio,
        matricula: MatriculaServicio,
        gestor: GestorAcademico,
    ) -> None:
        super().__init__(parent, style="Content.TFrame")
        self.cedula = cedula
        self.auth = auth
        self.matricula = matricula
        self.gestor = gestor

        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)

        page_header(self, "Mis calificaciones", "Consulte su rendimiento académico").grid(row=0, column=0, sticky="ew")

        tabla_card = Card(self, title="Calificaciones por materia")
        tabla_card.grid(row=1, column=0, sticky="ew", pady=(0, SPACE_MD))
        tabla_card.body.columnconfigure(0, weight=1)

        self.tabla, tree_wrap = create_treeview(
            tabla_card.body,
            ("materia", "nota", "estado"),
            {"materia": "Materia", "nota": "Nota", "estado": "Estado"},
            height=12,
            col_width=200,
        )
        tree_wrap.grid(row=0, column=0, sticky="ew")

        info_card = Card(self, title="Resumen académico")
        info_card.grid(row=2, column=0, sticky="nsew")
        info_card.body.rowconfigure(0, weight=1)
        info_card.body.columnconfigure(0, weight=1)

        self.texto = styled_text(info_card.body, height=10, wrap=tk.WORD)
        self.texto.grid(row=0, column=0, sticky="nsew")
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
            filas = []
            for materia, nota in estudiante.calificaciones.items():
                nombre = self.gestor.resolver_nombre_materia(materia)
                estado = "Aprobado" if nota >= NOTA_MINIMA_APROBACION else "Reprobado"
                filas.append((nombre, nota, estado))
            insertar_filas(self.tabla, filas)

            self.texto.insert(
                tk.END,
                f"Promedio general: {estudiante.promedio} — {estudiante.estado_academico}\n\n",
            )
            cursos = {c.id: c.nombre for c in self.matricula.listar_cursos()}
            for m in self.matricula.matriculas_de_estudiante(self.cedula):
                self.texto.insert(tk.END, f"Curso matriculado: {cursos.get(m.id_curso, m.id_curso)}\n")

            activas = self.gestor.materias_activas_estudiante(estudiante)
            if activas:
                self.texto.insert(tk.END, "\nMaterias activas:\n")
                for codigo, nombre, creditos in activas:
                    codigo_txt = f"{codigo} — " if codigo else ""
                    creditos_txt = f" ({creditos} créditos)" if creditos else ""
                    self.texto.insert(tk.END, f"• {codigo_txt}{nombre}{creditos_txt}\n")
        self.texto.config(state=tk.DISABLED)
