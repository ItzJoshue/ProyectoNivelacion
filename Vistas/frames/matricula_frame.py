import tkinter as tk
from tkinter import messagebox, ttk

from servicios.gestor_academico import GestorAcademico
from servicios.matricula_servicio import MatriculaServicio


class MatriculaFrame(ttk.Frame):
    def __init__(self, parent: tk.Widget, gestor: GestorAcademico, matricula: MatriculaServicio) -> None:
        super().__init__(parent, padding=10)
        self.gestor = gestor
        self.matricula = matricula
        self.var_est = tk.StringVar()
        self.var_cur = tk.StringVar()
        self.var_aula = tk.StringVar()

        ttk.Label(self, text="Gestión de Matrículas", font=("Segoe UI", 14, "bold")).pack(anchor=tk.W, pady=(0, 10))

        form = ttk.LabelFrame(self, text="Nueva matrícula", padding=10)
        form.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(form, text="Estudiante").grid(row=0, column=0, sticky=tk.W, pady=4)
        self.combo_est = ttk.Combobox(form, textvariable=self.var_est, width=55, state="readonly")
        self.combo_est.grid(row=0, column=1, padx=8, pady=4)

        ttk.Label(form, text="Curso").grid(row=1, column=0, sticky=tk.W, pady=4)
        self.combo_cur = ttk.Combobox(form, textvariable=self.var_cur, width=55, state="readonly")
        self.combo_cur.grid(row=1, column=1, padx=8, pady=4)

        ttk.Label(form, text="Aula").grid(row=2, column=0, sticky=tk.W, pady=4)
        self.combo_aula = ttk.Combobox(form, textvariable=self.var_aula, width=55, state="readonly")
        self.combo_aula.grid(row=2, column=1, padx=8, pady=4)

        ttk.Button(form, text="Recargar", command=self.cargar_listas).grid(row=3, column=0, pady=8)
        ttk.Button(form, text="Matricular", command=self._matricular).grid(row=3, column=1, sticky=tk.E, pady=8)

        self.tabla = ttk.Treeview(self, columns=("id", "estudiante", "curso", "aula"), show="headings", height=12)
        for c in ("id", "estudiante", "curso", "aula"):
            self.tabla.heading(c, text=c.upper())
            self.tabla.column(c, width=180)
        self.tabla.pack(fill=tk.BOTH, expand=True)
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
        est = {e.cedula: e.nombre_completo for e in self.gestor.listar_estudiantes()}
        cur = {c.id: c.nombre for c in self.matricula.listar_cursos()}
        aul = {a.id: a.codigo for a in self.matricula.listar_aulas()}
        for m in self.matricula.listar_matriculas():
            self.tabla.insert("", tk.END, values=(m.id, est.get(m.cedula_estudiante, m.cedula_estudiante), cur.get(m.id_curso, m.id_curso), aul.get(m.id_aula, m.id_aula)))
