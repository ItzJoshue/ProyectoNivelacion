import tkinter as tk
from tkinter import messagebox, ttk

from servicios.gestor_academico import GestorAcademico


class CalificacionesFrame(ttk.Frame):
    def __init__(self, parent: tk.Widget, gestor: GestorAcademico) -> None:
        super().__init__(parent, padding=10)
        self.gestor = gestor
        self.var_cedula = tk.StringVar()
        self.var_materia = tk.StringVar()
        self.var_nota = tk.StringVar()

        form = ttk.LabelFrame(self, text="Registrar calificación", padding=10)
        form.pack(fill=tk.X, pady=(0, 10))
        for i, (lbl, var) in enumerate(
            [
                ("Cédula:", self.var_cedula),
                ("Materia:", self.var_materia),
                ("Nota (0-10):", self.var_nota),
            ]
        ):
            ttk.Label(form, text=lbl).grid(row=i, column=0, sticky=tk.W, pady=3)
            ttk.Entry(form, textvariable=var, width=30).grid(row=i, column=1, padx=8, pady=3)
        ttk.Button(form, text="Guardar", command=self._guardar).grid(row=3, column=0, columnspan=2, pady=8)

        self.texto = tk.Text(self, height=20, wrap=tk.WORD)
        self.texto.pack(fill=tk.BOTH, expand=True)
        self.refrescar()

    def refrescar(self) -> None:
        self.texto.config(state=tk.NORMAL)
        self.texto.delete("1.0", tk.END)
        estudiantes = self.gestor.listar_estudiantes()
        if not estudiantes:
            self.texto.insert(tk.END, "No hay estudiantes registrados.\n")
        else:
            for resumen in self.gestor.obtener_resumenes_personas(estudiantes):
                self.texto.insert(tk.END, f"• {resumen}\n")
        self.texto.config(state=tk.DISABLED)

    def _guardar(self) -> None:
        try:
            self.gestor.registrar_calificacion(
                self.var_cedula.get().strip(),
                self.var_materia.get().strip(),
                float(self.var_nota.get()),
            )
            self.var_nota.set("")
            self.refrescar()
            messagebox.showinfo("Éxito", "Calificación registrada.")
        except (ValueError, KeyError) as e:
            messagebox.showerror("Error", str(e))
