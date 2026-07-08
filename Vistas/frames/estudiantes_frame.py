import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from servicios.contenedor import ContenedorAplicacion
from Vistas.ui.components import (
    Card,
    SPACE_MD,
    button_row,
    create_treeview,
    form_field,
    insertar_filas,
    page_header,
)


class EstudiantesFrame(ttk.Frame):
    """CRUD de estudiantes + import/export Excel (solo docente)."""

    def __init__(self, parent: tk.Widget, contenedor: ContenedorAplicacion) -> None:
        super().__init__(parent, style="Content.TFrame")
        self.contenedor = contenedor
        self.vars: dict[str, tk.StringVar] = {}

        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)

        page_header(self, "Estudiantes", "Administre el registro académico de estudiantes").grid(
            row=0, column=0, sticky="ew"
        )

        form_card = Card(self, title="Datos del estudiante")
        form_card.grid(row=1, column=0, sticky="ew", pady=(0, SPACE_MD))
        form_card.body.columnconfigure(0, weight=1)
        form_card.body.columnconfigure(1, weight=1)

        campos = [
            ("Cédula", "cedula"),
            ("Nombre", "nombre"),
            ("Apellido", "apellido"),
            ("Carrera", "carrera"),
            ("Email", "email"),
        ]
        for i, (lbl, key) in enumerate(campos):
            var = tk.StringVar()
            self.vars[key] = var
            container, _ = form_field(form_card.body, lbl, var, width=28)
            container.grid(row=i // 2, column=i % 2, sticky="ew", padx=(0, 12) if i % 2 == 0 else (12, 0))

        acciones = ttk.Frame(form_card.body, style="Card.TFrame")
        acciones.grid(row=3, column=0, columnspan=2, sticky="w", pady=(8, 0))
        button_row(
            acciones,
            [
                ("Registrar", self._registrar, "primary"),
                ("Actualizar", self._actualizar, "secondary"),
                ("Eliminar", self._eliminar, "danger"),
                ("Limpiar", self._limpiar, "secondary"),
            ],
        ).pack(anchor=tk.W)

        excel = ttk.Frame(form_card.body, style="Card.TFrame")
        excel.grid(row=4, column=0, columnspan=2, sticky="w", pady=(12, 0))
        button_row(
            excel,
            [
                ("Importar Excel", self._importar, "secondary"),
                ("Exportar Excel", self._exportar, "secondary"),
            ],
        ).pack(anchor=tk.W)

        tabla_card = Card(self, title="Listado de estudiantes")
        tabla_card.grid(row=2, column=0, sticky="nsew")
        tabla_card.body.rowconfigure(0, weight=1)
        tabla_card.body.columnconfigure(0, weight=1)

        cols = ("cedula", "nombre", "apellido", "carrera", "email", "promedio", "estado")
        headings = {
            "cedula": "Cédula",
            "nombre": "Nombre",
            "apellido": "Apellido",
            "carrera": "Carrera",
            "email": "Email",
            "promedio": "Promedio",
            "estado": "Estado",
        }
        self.tabla, tree_wrap = create_treeview(tabla_card.body, cols, headings, height=22, col_width=140)
        tree_wrap.grid(row=0, column=0, sticky="nsew")
        self.tabla.bind("<<TreeviewSelect>>", self._seleccionar)
        self.refrescar()

    def refrescar(self) -> None:
        for i in self.tabla.get_children():
            self.tabla.delete(i)
        filas = []
        for e in self.contenedor.gestor.listar_estudiantes():
            d = e.to_dict()
            filas.append(
                (
                    d["cedula"],
                    d["nombre"],
                    d["apellido"],
                    d["carrera"],
                    d["email"],
                    d["promedio"],
                    e.estado_academico,
                )
            )
        insertar_filas(self.tabla, filas)

    def _datos(self) -> dict:
        return {k: v.get().strip() for k, v in self.vars.items()}

    def _limpiar(self) -> None:
        for v in self.vars.values():
            v.set("")

    def _seleccionar(self, _=None) -> None:
        sel = self.tabla.selection()
        if not sel:
            return
        vals = self.tabla.item(sel[0], "values")
        for k, v in zip(("cedula", "nombre", "apellido", "carrera", "email"), vals):
            self.vars[k].set(v)

    def _registrar(self) -> None:
        try:
            self.contenedor.gestor.registrar_estudiante(self._datos())
            self.refrescar()
            self._limpiar()
            messagebox.showinfo("Éxito", "Estudiante registrado.")
        except (ValueError, KeyError) as e:
            messagebox.showerror("Error", str(e))

    def _actualizar(self) -> None:
        try:
            self.contenedor.gestor.actualizar_estudiante(self._datos())
            self.refrescar()
            messagebox.showinfo("Éxito", "Estudiante actualizado.")
        except (ValueError, KeyError) as e:
            messagebox.showerror("Error", str(e))

    def _eliminar(self) -> None:
        ced = self.vars["cedula"].get().strip()
        if not ced:
            return
        if messagebox.askyesno("Confirmar", f"¿Eliminar {ced}?") and self.contenedor.gestor.eliminar_estudiante(ced):
            self.refrescar()
            self._limpiar()

    def _importar(self) -> None:
        ruta = filedialog.askopenfilename(filetypes=[("Excel", "*.xlsx")])
        if ruta:
            try:
                n = self.contenedor.gestor.importar_estudiantes_excel(ruta)
                self.refrescar()
                messagebox.showinfo("Importación", f"{n} estudiante(s) importados.")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def _exportar(self) -> None:
        ruta = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel", "*.xlsx")])
        if ruta:
            try:
                n = self.contenedor.gestor.exportar_estudiantes_excel(ruta)
                messagebox.showinfo("Exportación", f"{n} estudiante(s) exportados.")
            except Exception as e:
                messagebox.showerror("Error", str(e))
