import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from Utilidades.almacenamiento import leer_json, guardar_json, nuevo_id

class MatriculaFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#eaf6ff")

        tk.Label(
            self, text="Gestión de Matrículas", bg="#eaf6ff", fg="black",
            font=("Arial", 18, "bold")
        ).pack(anchor="w", pady=(0, 12))

        formulario = tk.Frame(self, bg="white", padx=10, pady=10)
        formulario.pack(fill="x")

        self.est_var = tk.StringVar()
        self.cur_var = tk.StringVar()
        self.aula_var = tk.StringVar()

        tk.Label(formulario, text="Estudiante", bg="white").grid(row=0, column=0, sticky="w", padx=6, pady=6)
        self.combo_est = ttk.Combobox(formulario, textvariable=self.est_var, width=60, state="readonly")
        self.combo_est.grid(row=0, column=1, padx=6, pady=6)

        tk.Label(formulario, text="Curso", bg="white").grid(row=1, column=0, sticky="w", padx=6, pady=6)
        self.combo_cur = ttk.Combobox(formulario, textvariable=self.cur_var, width=60, state="readonly")
        self.combo_cur.grid(row=1, column=1, padx=6, pady=6)

        tk.Label(formulario, text="Aula", bg="white").grid(row=2, column=0, sticky="w", padx=6, pady=6)
        self.combo_aula = ttk.Combobox(formulario, textvariable=self.aula_var, width=60, state="readonly")
        self.combo_aula.grid(row=2, column=1, padx=6, pady=6)

        tk.Button(formulario, text="Recargar listas", width=16, command=self.cargar_listas).grid(row=3, column=0, padx=6, pady=8)
        tk.Button(formulario, text="Matricular", width=16, command=self.matricular).grid(row=3, column=1, sticky="e", padx=6, pady=8)

        self.tabla = ttk.Treeview(self, columns=("id", "estudiante", "curso", "aula"), show="headings")
        for col in ("id", "estudiante", "curso", "aula"):
            self.tabla.heading(col, text=col.upper())
            self.tabla.column(col, width=200, anchor="center")
        self.tabla.pack(fill="both", expand=True, pady=10)

        self.cargar_listas()
        self.refrescar()

    def cargar_listas(self):
        self.estudiantes = leer_json("estudiantes")
        self.cursos = leer_json("cursos")
        self.aulas = leer_json("aulas")

        self.combo_est["values"] = [
            f'{e.get("id")} | {e.get("nombre")} | {e.get("cedula")}' for e in self.estudiantes
        ]
        self.combo_cur["values"] = [
            f'{c.get("id")} | {c.get("nombre")} | cupos: {c.get("cupos")}' for c in self.cursos
        ]
        self.combo_aula["values"] = [
            f'{a.get("id")} | {a.get("codigo")} | capacidad: {a.get("capacidad")}' for a in self.aulas
        ]

    def obtener_id(self, texto):
        return texto.split("|")[0].strip() if texto else ""

    def matricular(self):
        estudiante_id = self.obtener_id(self.est_var.get())
        curso_id = self.obtener_id(self.cur_var.get())
        aula_id = self.obtener_id(self.aula_var.get())

        if not estudiante_id or not curso_id or not aula_id:
            messagebox.showwarning("Validación", "Debes seleccionar estudiante, curso y aula.")
            return

        matriculas = leer_json("matriculas")

        if any(m.get("estudiante_id") == estudiante_id and m.get("curso_id") == curso_id for m in matriculas):
            messagebox.showwarning("Duplicado", "Este estudiante ya está matriculado en ese curso.")
            return

        cursos = leer_json("cursos")
        curso = next((c for c in cursos if c.get("id") == curso_id), None)

        if curso:
            try:
                cupos = int(curso.get("cupos", "0"))
            except Exception:
                cupos = 0

            ocupados = len([m for m in matriculas if m.get("curso_id") == curso_id])
            if ocupados >= cupos:
                messagebox.showwarning("Sin cupos", "El curso seleccionado ya no tiene cupos disponibles.")
                return

        nueva = {
            "id": nuevo_id("MAT"),
            "estudiante_id": estudiante_id,
            "curso_id": curso_id,
            "aula_id": aula_id
        }

        matriculas.append(nueva)

        if guardar_json("matriculas", matriculas):
            self.refrescar()
            messagebox.showinfo("Correcto", "Matrícula registrada correctamente.")

    def refrescar(self):
        for item in self.tabla.get_children():
            self.tabla.delete(item)

        estudiantes = {e.get("id"): e.get("nombre") for e in leer_json("estudiantes")}
        cursos = {c.get("id"): c.get("nombre") for c in leer_json("cursos")}
        aulas = {a.get("id"): a.get("codigo") for a in leer_json("aulas")}

        for m in leer_json("matriculas"):
            self.tabla.insert("", "end", values=(
                m.get("id", ""),
                estudiantes.get(m.get("estudiante_id"), ""),
                cursos.get(m.get("curso_id"), ""),
                aulas.get(m.get("aula_id"), "")
            ))