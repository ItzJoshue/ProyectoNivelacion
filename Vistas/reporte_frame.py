import tkinter as tk
from tkinter import messagebox
from Utilidades.almacenamiento import leer_json, DATA_DIR


class ReporteFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#eaf6ff")

        tk.Label(
            self, text="Reportes", bg="#eaf6ff", fg="black",
            font=("Arial", 18, "bold")
        ).pack(anchor="w", pady=(0, 12))

        botones = tk.Frame(self, bg="#eaf6ff")
        botones.pack(fill="x", pady=5)

        tk.Button(botones, text="Generar reporte", width=18, command=self.generar).pack(side="left", padx=4)
        tk.Button(botones, text="Ver carpeta JSON", width=18, command=self.ver_ruta).pack(side="left", padx=4)

        self.texto = tk.Text(self, bg="white", fg="black", font=("Consolas", 10))
        self.texto.pack(fill="both", expand=True, pady=8)

    def ver_ruta(self):
        messagebox.showinfo("Carpeta de datos", f"Los JSON se guardan en:\n{DATA_DIR}")

    def generar(self):
        self.texto.delete("1.0", "end")

        estudiantes = leer_json("estudiantes")
        profesores = leer_json("profesores")
        aulas = leer_json("aulas")
        cursos = leer_json("cursos")
        postulantes = leer_json("postulantes")
        matriculas = leer_json("matriculas")

        self.texto.insert("end", "===== REPORTE GENERAL ULEAM =====\n\n")
        self.texto.insert("end", f"Carpeta JSON: {DATA_DIR}\n\n")
        self.texto.insert("end", f"Estudiantes:  {len(estudiantes)}\n")
        self.texto.insert("end", f"Profesores:   {len(profesores)}\n")
        self.texto.insert("end", f"Aulas:        {len(aulas)}\n")
        self.texto.insert("end", f"Cursos:       {len(cursos)}\n")
        self.texto.insert("end", f"Postulantes:  {len(postulantes)}\n")
        self.texto.insert("end", f"Matrículas:   {len(matriculas)}\n\n")

        self.texto.insert("end", "===== MATRÍCULAS =====\n")
        estudiantes_dict = {e.get("id"): e.get("nombre") for e in estudiantes}
        cursos_dict = {c.get("id"): c.get("nombre") for c in cursos}
        aulas_dict = {a.get("id"): a.get("codigo") for a in aulas}

        if not matriculas:
            self.texto.insert("end", "No hay matrículas registradas.\n")
        else:
            for m in matriculas:
                self.texto.insert(
                    "end",
                    f"- {estudiantes_dict.get(m.get('estudiante_id'), 'N/D')} | "
                    f"{cursos_dict.get(m.get('curso_id'), 'N/D')} | "
                    f"Aula {aulas_dict.get(m.get('aula_id'), 'N/D')}\n"
                )