import tkinter as tk
from tkinter import messagebox, ttk

from infraestructura.utilidades.almacenamiento import guardar_json, leer_json, nuevo_id
from Vistas.ui.components import (
    Card,
    SPACE_MD,
    button_row,
    create_treeview,
    form_field,
    insertar_filas,
    page_header,
)


class CrudJsonFrame(ttk.Frame):
    """CRUD genérico sobre JSON (módulo heredado de rama Modulosss)."""

    def __init__(
        self,
        parent: tk.Widget,
        titulo: str,
        archivo: str,
        campos: list[str],
        columnas: list[str],
    ) -> None:
        super().__init__(parent, style="Content.TFrame")
        self.archivo = archivo
        self.campos = campos
        self.columnas = columnas
        self.vars: dict[str, tk.StringVar] = {}
        self.id_sel: str | None = None

        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)

        page_header(self, titulo, "Gestione los registros del módulo").grid(row=0, column=0, sticky="ew")

        form_card = Card(self, title="Formulario")
        form_card.grid(row=1, column=0, sticky="ew", pady=(0, SPACE_MD))
        cols_per_row = min(3, max(1, len(campos)))
        for col_i in range(cols_per_row):
            form_card.body.columnconfigure(col_i, weight=1)

        for i, c in enumerate(campos):
            var = tk.StringVar()
            self.vars[c] = var
            container, _ = form_field(form_card.body, c.capitalize(), var, width=24)
            container.grid(
                row=i // cols_per_row,
                column=i % cols_per_row,
                sticky="ew",
                padx=(0, 8) if i % cols_per_row != cols_per_row - 1 else 0,
            )

        acciones = ttk.Frame(form_card.body, style="Card.TFrame")
        acciones.grid(row=(len(campos) + cols_per_row - 1) // cols_per_row, column=0, columnspan=cols_per_row, sticky="w", pady=(8, 0))
        button_row(
            acciones,
            [
                ("Guardar", self._guardar, "primary"),
                ("Actualizar", self._actualizar, "secondary"),
                ("Eliminar", self._eliminar, "danger"),
                ("Limpiar", self._limpiar, "secondary"),
            ],
        ).pack(anchor=tk.W)

        tabla_card = Card(self, title="Registros")
        tabla_card.grid(row=2, column=0, sticky="nsew")
        tabla_card.body.rowconfigure(0, weight=1)
        tabla_card.body.columnconfigure(0, weight=1)

        self.tabla, tree_wrap = create_treeview(
            tabla_card.body,
            tuple(columnas),
            {c: c.upper() for c in columnas},
            height=14,
            col_width=130,
        )
        tree_wrap.grid(row=0, column=0, sticky="nsew")
        self.tabla.bind("<<TreeviewSelect>>", self._seleccionar)
        self.refrescar()

    def refrescar(self) -> None:
        for i in self.tabla.get_children():
            self.tabla.delete(i)
        filas = [[reg.get(c, "") for c in self.columnas] for reg in leer_json(self.archivo)]
        insertar_filas(self.tabla, [tuple(f) for f in filas])

    def _seleccionar(self, _=None) -> None:
        sel = self.tabla.selection()
        if not sel:
            return
        vals = self.tabla.item(sel[0], "values")
        self.id_sel = vals[0] if vals else None
        datos = leer_json(self.archivo)
        reg = next((d for d in datos if d.get("id") == self.id_sel), None)
        if reg:
            for c in self.campos:
                self.vars[c].set(str(reg.get(c, "")))

    def _limpiar(self) -> None:
        self.id_sel = None
        for v in self.vars.values():
            v.set("")

    def _guardar(self) -> None:
        datos = leer_json(self.archivo)
        nuevo = {"id": nuevo_id(self.archivo[:3].upper())}
        for c, v in self.vars.items():
            nuevo[c] = v.get().strip()
        datos.append(nuevo)
        guardar_json(self.archivo, datos)
        self.refrescar()
        self._limpiar()
        messagebox.showinfo("Éxito", "Registro guardado.")

    def _actualizar(self) -> None:
        if not self.id_sel:
            messagebox.showwarning("Aviso", "Seleccione un registro.")
            return
        datos = leer_json(self.archivo)
        for item in datos:
            if item.get("id") == self.id_sel:
                for c, v in self.vars.items():
                    item[c] = v.get().strip()
        guardar_json(self.archivo, datos)
        self.refrescar()
        messagebox.showinfo("Éxito", "Registro actualizado.")

    def _eliminar(self) -> None:
        if not self.id_sel:
            return
        datos = [d for d in leer_json(self.archivo) if d.get("id") != self.id_sel]
        guardar_json(self.archivo, datos)
        self.refrescar()
        self._limpiar()
