import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from servicios.gestor_academico import GestorAcademico


class EstudiantesFrame(ttk.Frame):
    """CRUD de estudiantes + import/export Excel (solo docente)."""

    def __init__(self, parent: tk.Widget, gestor: GestorAcademico) -> None:
        super().__init__(parent, padding=10)
        self.gestor = gestor
        self.vars: dict[str, tk.StringVar] = {}

        form = ttk.LabelFrame(self, text="Datos del estudiante", padding=10)
        form.pack(fill=tk.X, pady=(0, 10))

        for i, (lbl, key) in enumerate(
            [
                ("Cédula:", "cedula"),
                ("Nombre:", "nombre"),
                ("Apellido:", "apellido"),
                ("Carrera:", "carrera"),
                ("Email:", "email"),
            ]
        ):
            ttk.Label(form, text=lbl).grid(row=i, column=0, sticky=tk.W, pady=3)
            var = tk.StringVar()
            self.vars[key] = var
            ttk.Entry(form, textvariable=var, width=40).grid(row=i, column=1, padx=8, pady=3)

        btns = ttk.Frame(form)
        btns.grid(row=5, column=0, columnspan=2, pady=10, sticky=tk.W)
        for txt, cmd in [
            ("Registrar", self._registrar),
            ("Actualizar", self._actualizar),
            ("Eliminar", self._eliminar),
            ("Limpiar", self._limpiar),
        ]:
            ttk.Button(btns, text=txt, command=cmd).pack(side=tk.LEFT, padx=4)

        excel = ttk.Frame(self)
        excel.pack(fill=tk.X, pady=(0, 8))
        ttk.Button(excel, text="Importar Excel", command=self._importar).pack(side=tk.LEFT, padx=4)
        ttk.Button(excel, text="Exportar Excel", command=self._exportar).pack(side=tk.LEFT, padx=4)

        tabla_f = ttk.LabelFrame(self, text="Listado", padding=8)
        tabla_f.pack(fill=tk.BOTH, expand=True)
        cols = ("cedula", "nombre", "apellido", "carrera", "email", "promedio")
        self.tabla = ttk.Treeview(tabla_f, columns=cols, show="headings", height=12)
        for c, t in zip(cols, ["Cédula", "Nombre", "Apellido", "Carrera", "Email", "Promedio"]):
            self.tabla.heading(c, text=t)
            self.tabla.column(c, width=110)
        self.tabla.pack(fill=tk.BOTH, expand=True)
        self.tabla.bind("<<TreeviewSelect>>", self._seleccionar)
        self.refrescar()

    def refrescar(self) -> None:
        for i in self.tabla.get_children():
            self.tabla.delete(i)
        for e in self.gestor.listar_estudiantes():
            d = e.to_dict()
            self.tabla.insert("", tk.END, values=tuple(d[k] for k in ("cedula", "nombre", "apellido", "carrera", "email", "promedio")))

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
            self.gestor.registrar_estudiante(self._datos())
            self.refrescar()
            self._limpiar()
            messagebox.showinfo("Éxito", "Estudiante registrado.")
        except (ValueError, KeyError) as e:
            messagebox.showerror("Error", str(e))

    def _actualizar(self) -> None:
        try:
            self.gestor.actualizar_estudiante(self._datos())
            self.refrescar()
            messagebox.showinfo("Éxito", "Estudiante actualizado.")
        except (ValueError, KeyError) as e:
            messagebox.showerror("Error", str(e))

    def _eliminar(self) -> None:
        ced = self.vars["cedula"].get().strip()
        if not ced:
            return
        if messagebox.askyesno("Confirmar", f"¿Eliminar {ced}?") and self.gestor.eliminar_estudiante(ced):
            self.refrescar()
            self._limpiar()

    def _importar(self) -> None:
        ruta = filedialog.askopenfilename(filetypes=[("Excel", "*.xlsx")])
        if ruta:
            try:
                n = self.gestor.importar_estudiantes_excel(ruta)
                self.refrescar()
                messagebox.showinfo("Importación", f"{n} estudiante(s) importados.")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def _exportar(self) -> None:
        ruta = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel", "*.xlsx")])
        if ruta:
            try:
                n = self.gestor.exportar_estudiantes_excel(ruta)
                messagebox.showinfo("Exportación", f"{n} estudiante(s) exportados.")
            except Exception as e:
                messagebox.showerror("Error", str(e))
