import tkinter as tk
from tkinter import messagebox, ttk

from servicios.gestor_academico import GestorAcademico


class MateriasFrame(ttk.Frame):
    def __init__(self, parent: tk.Widget, gestor: GestorAcademico) -> None:
        super().__init__(parent, padding=10)
        self.gestor = gestor
        self.var_codigo = tk.StringVar()
        self.var_nombre = tk.StringVar()
        self.var_creditos = tk.StringVar(value="3")

        form = ttk.LabelFrame(self, text="Nueva materia", padding=10)
        form.pack(fill=tk.X, pady=(0, 10))
        for i, (lbl, var) in enumerate(
            [("Código:", self.var_codigo), ("Nombre:", self.var_nombre), ("Créditos:", self.var_creditos)]
        ):
            ttk.Label(form, text=lbl).grid(row=i, column=0, sticky=tk.W, pady=3)
            ttk.Entry(form, textvariable=var, width=30).grid(row=i, column=1, padx=8, pady=3)
        ttk.Button(form, text="Registrar", command=self._registrar).grid(row=3, column=0, columnspan=2, pady=8)

        self.tabla = ttk.Treeview(self, columns=("codigo", "nombre", "creditos"), show="headings", height=14)
        for c, t in zip(("codigo", "nombre", "creditos"), ["Código", "Nombre", "Créditos"]):
            self.tabla.heading(c, text=t)
            self.tabla.column(c, width=140)
        self.tabla.pack(fill=tk.BOTH, expand=True)
        self.refrescar()

    def refrescar(self) -> None:
        for i in self.tabla.get_children():
            self.tabla.delete(i)
        for m in self.gestor.listar_materias():
            self.tabla.insert("", tk.END, values=(m.codigo, m.nombre, m.creditos))

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
