import tkinter as tk
from tkinter import ttk

from servicios.contenedor import ContenedorAplicacion
from Vistas.ui.components import Card, SPACE_MD, create_treeview, insertar_filas, page_header, styled_text


class MisCalificacionesFrame(ttk.Frame):
    """Vista restringida: solo las calificaciones del estudiante autenticado."""

    def __init__(
        self,
        parent: tk.Widget,
        cedula: str,
        contenedor: ContenedorAplicacion,
    ) -> None:
        super().__init__(parent, style="Content.TFrame")
        self.cedula = cedula
        self.contenedor = contenedor

        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)

        page_header(self, "Mis calificaciones", "Consulte su rendimiento académico").grid(row=0, column=0, sticky="ew")

        tabla_card = Card(self, title="Calificaciones por materia")
        tabla_card.grid(row=1, column=0, sticky="ew", pady=(0, SPACE_MD))
        tabla_card.body.columnconfigure(0, weight=1)

        self.tabla, tree_wrap = create_treeview(
            tabla_card.body,
            ("materia", "nota"),
            {"materia": "Materia", "nota": "Nota"},
            height=8,
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

        estudiante = self.contenedor.obtener_perfil_estudiante(self.cedula)
        if estudiante is None:
            self.texto.insert(tk.END, "Sin datos académicos.")
        else:
            filas = [(materia, nota) for materia, nota in estudiante.calificaciones.items()]
            insertar_filas(self.tabla, filas)
            self.texto.insert(tk.END, f"Promedio general: {estudiante.promedio}\n\n")
            cursos = {c.id: c.nombre for c in self.contenedor.matricula.listar_cursos()}
            for m in self.contenedor.matricula.matriculas_de_estudiante(self.cedula):
                self.texto.insert(tk.END, f"Curso matriculado: {cursos.get(m.id_curso, m.id_curso)}\n")
        self.texto.config(state=tk.DISABLED)
