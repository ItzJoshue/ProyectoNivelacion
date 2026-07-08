import tkinter as tk
from tkinter import ttk

from servicios.contenedor import ContenedorAplicacion
from Vistas.ui.components import Card, SPACE_MD, create_treeview, insertar_filas, page_header, styled_text


class MiPerfilFrame(ttk.Frame):
    """Vista restringida: el estudiante solo ve su propio perfil."""

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

        page_header(self, "Mi perfil", "Información académica de su cuenta").grid(row=0, column=0, sticky="ew")

        datos_card = Card(self, title="Datos personales")
        datos_card.grid(row=1, column=0, sticky="ew", pady=(0, SPACE_MD))
        datos_card.body.columnconfigure(0, weight=1)

        self.texto = styled_text(datos_card.body, height=8, wrap=tk.WORD)
        self.texto.grid(row=0, column=0, sticky="ew")

        materias_card = Card(self, title="Materias activas")
        materias_card.grid(row=2, column=0, sticky="nsew")
        materias_card.body.rowconfigure(0, weight=1)
        materias_card.body.columnconfigure(0, weight=1)

        self.tabla, tree_wrap = create_treeview(
            materias_card.body,
            ("codigo", "nombre", "creditos"),
            {"codigo": "Código", "nombre": "Nombre", "creditos": "Créditos"},
            height=12,
            col_width=180,
        )
        tree_wrap.grid(row=0, column=0, sticky="nsew")
        self.refrescar()

    def refrescar(self) -> None:
        for i in self.tabla.get_children():
            self.tabla.delete(i)
        self.texto.config(state=tk.NORMAL)
        self.texto.delete("1.0", tk.END)
        estudiante = self.contenedor.obtener_perfil_estudiante(self.cedula)
        if estudiante is None:
            self.texto.insert(tk.END, "No se encontró su perfil académico.")
        else:
            self.texto.insert(tk.END, f"{estudiante.obtener_resumen()}\n\n")
            self.texto.insert(tk.END, f"Carrera: {estudiante.carrera}\n")
            self.texto.insert(tk.END, f"Email: {estudiante.email}\n")
            mats = self.contenedor.matricula.matriculas_de_estudiante(self.cedula)
            self.texto.insert(tk.END, f"\nMatrículas activas: {len(mats)}\n")

            activas = self.contenedor.gestor.materias_activas_estudiante(estudiante)
            if activas:
                insertar_filas(self.tabla, activas)
            else:
                self.tabla.insert("", tk.END, values=("", "No tiene materias activas registradas", ""))
        self.texto.config(state=tk.DISABLED)
