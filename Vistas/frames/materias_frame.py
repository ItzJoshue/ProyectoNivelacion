import tkinter as tk
from tkinter import messagebox, ttk

from servicios.gestor_academico import GestorAcademico
from Vistas.ui.components import (
    Card,
    SPACE_MD,
    button_row,
    create_treeview,
    form_field,
    insertar_filas,
    page_header,
)


class MateriasFrame(ttk.Frame):
    def __init__(self, parent: tk.Widget, gestor: GestorAcademico) -> None:
        super().__init__(parent, style="Content.TFrame")
        self.gestor = gestor
        self.var_codigo = tk.StringVar()
        self.var_nombre = tk.StringVar()
        self.var_creditos = tk.StringVar(value="3")

        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)

        page_header(self, "Materias", "Registre y consulte las materias de nivelación").grid(row=0, column=0, sticky="ew")

        form_card = Card(self, title="Nueva materia")
        form_card.grid(row=1, column=0, sticky="ew", pady=(0, SPACE_MD))
        form_card.body.columnconfigure(0, weight=1)
        form_card.body.columnconfigure(1, weight=1)
        form_card.body.columnconfigure(2, weight=1)

        codigo_frame, _ = form_field(
            form_card.body,
            "Código",
            self.var_codigo,
            width=22
        )
        codigo_frame.grid(row=0, column=0, sticky="ew", padx=(0, 8))

        nombre_frame, _ = form_field(
            form_card.body,
            "Nombre",
            self.var_nombre,
            width=22
        )
        nombre_frame.grid(row=0, column=1, sticky="ew", padx=8)

        creditos_frame, _ = form_field(
            form_card.body,
            "Créditos",
            self.var_creditos,
            width=22
        )
        creditos_frame.grid(row=0, column=2, sticky="ew", padx=(8, 0))

        acciones = ttk.Frame(form_card.body, style="Card.TFrame")
        acciones.grid(row=1, column=0, columnspan=3, sticky="w", pady=(4, 0))
        button_row(acciones, [("Registrar", self._registrar, "primary")]).pack(anchor=tk.W)

        tabla_card = Card(self, title="Materias registradas")
        tabla_card.grid(row=2, column=0, sticky="nsew")
        tabla_card.body.rowconfigure(0, weight=1)
        tabla_card.body.columnconfigure(0, weight=1)

        cols = ("codigo", "nombre", "creditos")
        headings = {"codigo": "Código", "nombre": "Nombre", "creditos": "Créditos"}
        self.tabla, tree_wrap = create_treeview(tabla_card.body, cols, headings, height=16, col_width=160)
        tree_wrap.grid(row=0, column=0, sticky="nsew")
        self.refrescar()

    def refrescar(self) -> None:
        for i in self.tabla.get_children():
            self.tabla.delete(i)
        filas = [(m.codigo, m.nombre, m.creditos) for m in self.gestor.listar_materias()]
        insertar_filas(self.tabla, filas)

    def _registrar(self) -> None:
        try:
            self.gestor.registrar_materia(
                self.var_codigo.get().strip(),
                self.var_nombre.get().strip(),
                int(self.var_creditos.get()),
            )
            self.var_codigo.set("")
            self.var_nombre.set("")
            self.var_creditos.set("3")
            self.refrescar()
            messagebox.showinfo("Éxito", "Materia registrada.")
        except (ValueError, KeyError) as e:
            messagebox.showerror("Error", str(e))
