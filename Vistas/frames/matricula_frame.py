import tkinter as tk
from tkinter import messagebox, ttk

from servicios.gestor_academico import GestorAcademico
from servicios.matricula_servicio import MatriculaServicio
from Vistas.ui.components import (
    Card,
    SPACE_MD,
    button_row,
    create_treeview,
    form_field,
    insertar_filas,
    page_header,
)


class MatriculaFrame(ttk.Frame):
    def __init__(self, parent: tk.Widget, gestor: GestorAcademico, matricula: MatriculaServicio) -> None:
        super().__init__(parent, style="Content.TFrame")
        self.gestor = gestor
        self.matricula = matricula
        self.var_est = tk.StringVar()
        self.var_cur = tk.StringVar()
        self.var_aula = tk.StringVar()

        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)

        page_header(self, "Gestión de Matrículas", "Asigne estudiantes a cursos y aulas").grid(
            row=0, column=0, sticky="ew"
        )

        form_card = Card(self, title="Nueva matrícula")
        form_card.grid(row=1, column=0, sticky="ew", pady=(0, SPACE_MD))
        form_card.body.columnconfigure(0, weight=1)

        est_container, self.combo_est = form_field(
            form_card.body, "Estudiante", self.var_est, combobox=True, readonly=True, width=52
        )
        est_container.grid(row=0, column=0, sticky="ew")

        cur_container, self.combo_cur = form_field(
            form_card.body, "Curso", self.var_cur, combobox=True, readonly=True, width=52
        )
        cur_container.grid(row=1, column=0, sticky="ew")

        aula_container, self.combo_aula = form_field(
            form_card.body, "Aula", self.var_aula, combobox=True, readonly=True, width=52
        )
        aula_container.grid(row=2, column=0, sticky="ew")

        acciones = ttk.Frame(form_card.body, style="Card.TFrame")
        acciones.grid(row=3, column=0, sticky="w", pady=(4, 0))
        button_row(
            acciones,
            [
                ("Recargar listas", self.cargar_listas, "secondary"),
                ("Matricular", self._matricular, "primary"),
            ],
        ).pack(anchor=tk.W)

        tabla_card = Card(self, title="Matrículas registradas")
        tabla_card.grid(row=2, column=0, sticky="nsew")
        tabla_card.body.rowconfigure(0, weight=1)
        tabla_card.body.columnconfigure(0, weight=1)

        cols = ("id", "estudiante", "curso", "aula", "promedio", "estado")
        headings = {
            "id": "ID",
            "estudiante": "Estudiante",
            "curso": "Curso",
            "aula": "Aula",
            "promedio": "Promedio",
            "estado": "Estado",
        }
        self.tabla, tree_wrap = create_treeview(tabla_card.body, cols, headings, height=20, col_width=150)
        tree_wrap.grid(row=0, column=0, sticky="nsew")
        self.cargar_listas()
        self.refrescar()

    def cargar_listas(self) -> None:
        estudiantes = self.gestor.listar_estudiantes()
        cursos = self.matricula.listar_cursos()
        aulas = self.matricula.listar_aulas()
        self.combo_est["values"] = [f"{e.cedula} | {e.nombre_completo}" for e in estudiantes]
        self.combo_cur["values"] = [f"{c.id} | {c.nombre} | cupos: {c.cupos}" for c in cursos]
        self.combo_aula["values"] = [f"{a.id} | {a.codigo} | cap: {a.capacidad}" for a in aulas]

    @staticmethod
    def _id(texto: str) -> str:
        return texto.split("|")[0].strip() if texto else ""

    def _matricular(self) -> None:
        try:
            self.matricula.matricular(
                self._id(self.var_est.get()),
                self._id(self.var_cur.get()),
                self._id(self.var_aula.get()),
            )
            self.refrescar()
            messagebox.showinfo("Éxito", "Matrícula registrada.")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def refrescar(self) -> None:
        for i in self.tabla.get_children():
            self.tabla.delete(i)
        est = {e.cedula: e for e in self.gestor.listar_estudiantes()}
        cur = {c.id: c.nombre for c in self.matricula.listar_cursos()}
        aul = {a.id: a.codigo for a in self.matricula.listar_aulas()}
        filas = []
        for m in self.matricula.listar_matriculas():
            estudiante = est.get(m.cedula_estudiante)
            nombre = estudiante.nombre_completo if estudiante else m.cedula_estudiante
            promedio = estudiante.promedio if estudiante else 0.0
            estado = estudiante.estado_academico if estudiante else "Sin calificar"
            filas.append(
                (
                    m.id,
                    nombre,
                    cur.get(m.id_curso, m.id_curso),
                    aul.get(m.id_aula, m.id_aula),
                    promedio,
                    estado,
                )
            )
        insertar_filas(self.tabla, filas)
