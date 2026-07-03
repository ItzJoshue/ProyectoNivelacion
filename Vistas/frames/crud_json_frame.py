import tkinter as tk
from tkinter import messagebox, ttk

from infraestructura.utilidades.almacenamiento import guardar_json, leer_json, nuevo_id


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
        super().__init__(parent, padding=10)
        self.archivo = archivo
        self.campos = campos
        self.columnas = columnas
        self.vars: dict[str, tk.StringVar] = {}
        self.id_sel: str | None = None

        ttk.Label(self, text=titulo, font=("Segoe UI", 14, "bold")).pack(anchor=tk.W, pady=(0, 10))

        form = ttk.LabelFrame(self, text="Formulario", padding=10)
        form.pack(fill=tk.X, pady=(0, 8))
        for i, c in enumerate(campos):
            ttk.Label(form, text=c.capitalize()).grid(row=i, column=0, sticky=tk.W, pady=3)
            var = tk.StringVar()
            self.vars[c] = var
            ttk.Entry(form, textvariable=var, width=40).grid(row=i, column=1, padx=8, pady=3)

        btns = ttk.Frame(form)
        btns.grid(row=len(campos), column=0, columnspan=2, pady=8)
        for txt, cmd in [("Guardar", self._guardar), ("Actualizar", self._actualizar), ("Eliminar", self._eliminar), ("Limpiar", self._limpiar)]:
            ttk.Button(btns, text=txt, command=cmd).pack(side=tk.LEFT, padx=4)

        self.tabla = ttk.Treeview(self, columns=columnas, show="headings", height=12)
        for col in columnas:
            self.tabla.heading(col, text=col.upper())
            self.tabla.column(col, width=130)
        self.tabla.pack(fill=tk.BOTH, expand=True)
        self.tabla.bind("<<TreeviewSelect>>", self._seleccionar)
        self.refrescar()

    def refrescar(self) -> None:
        for i in self.tabla.get_children():
            self.tabla.delete(i)
        for reg in leer_json(self.archivo):
            self.tabla.insert("", tk.END, values=[reg.get(c, "") for c in self.columnas])

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
