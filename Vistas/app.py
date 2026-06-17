import tkinter as tk
from Vistas.Crud_Frame import CrudFrame
from Vistas.Matricula_Frame import MatriculaFrame
from Vistas.reporte_frame import ReporteFrame
from Utilidades.almacenamiento import iniciar_json

class App:
    def __init__(self, root):
        iniciar_json()

        self.root = root
        self.root.title("Sistema Académico ULEAM - G4")
        self.root.geometry("1120x720")
        self.root.configure(bg="#eaf6ff")

        encabezado = tk.Frame(root, bg="#eaf6ff")
        encabezado.pack(fill="x", padx=24, pady=14)

        tk.Label(
            encabezado, text="Sistema Académico ULEAM", bg="#eaf6ff",
            fg="black", font=("Arial", 22, "bold")
        ).pack(side="left")

        tk.Label(
            encabezado, text="G4", bg="#eaf6ff",
            fg="black", font=("Arial", 12)
        ).pack(side="right")

        cuerpo = tk.Frame(root, bg="#eaf6ff")
        cuerpo.pack(fill="both", expand=True, padx=14, pady=10)

        menu = tk.Frame(cuerpo, bg="#bdeaff", width=195)
        menu.pack(side="left", fill="y", padx=(0, 20))
        menu.pack_propagate(False)

        self.contenido = tk.Frame(cuerpo, bg="#eaf6ff")
        self.contenido.pack(side="left", fill="both", expand=True)

        opciones = [
            ("Estudiantes", self.ver_estudiantes),
            ("Profesores", self.ver_profesores),
            ("Aulas", self.ver_aulas),
            ("Cursos", self.ver_cursos),
            ("Postulantes", self.ver_postulantes),
            ("Matrículas", self.ver_matriculas),
            ("Reportes", self.ver_reportes),
        ]

        for texto, comando in opciones:
            tk.Button(
                menu, text=texto, command=comando, bg="white", fg="black",
                width=18, height=2, relief="flat"
            ).pack(pady=7)

        self.ver_estudiantes()

    def limpiar_contenido(self):
        for widget in self.contenido.winfo_children():
            widget.destroy()

    def ver_estudiantes(self):
        self.limpiar_contenido()
        frame = CrudFrame(
            self.contenido,
            "Gestión de Estudiantes",
            "estudiantes",
            ["nombre", "cedula", "carrera", "correo"],
            ["id", "nombre", "cedula", "carrera", "correo"]
        )
        frame.pack(fill="both", expand=True)

    def ver_profesores(self):
        self.limpiar_contenido()
        frame = CrudFrame(
            self.contenido,
            "Gestión de Profesores",
            "profesores",
            ["nombre", "cedula", "materia", "correo"],
            ["id", "nombre", "cedula", "materia", "correo"]
        )
        frame.pack(fill="both", expand=True)

    def ver_aulas(self):
        self.limpiar_contenido()
        frame = CrudFrame(
            self.contenido,
            "Gestión de Aulas",
            "aulas",
            ["codigo", "capacidad"],
            ["id", "codigo", "capacidad"]
        )
        frame.pack(fill="both", expand=True)

    def ver_cursos(self):
        self.limpiar_contenido()
        frame = CrudFrame(
            self.contenido,
            "Gestión de Cursos",
            "cursos",
            ["nombre", "carrera", "cupos"],
            ["id", "nombre", "carrera", "cupos"]
        )
        frame.pack(fill="both", expand=True)

    def ver_postulantes(self):
        self.limpiar_contenido()
        frame = CrudFrame(
            self.contenido,
            "Gestión de Postulantes",
            "postulantes",
            ["nombre", "cedula", "carrera", "puntaje", "correo"],
            ["id", "nombre", "cedula", "carrera", "puntaje", "correo"]
        )
        frame.pack(fill="both", expand=True)

    def ver_matriculas(self):
        self.limpiar_contenido()
        frame = MatriculaFrame(self.contenido)
        frame.pack(fill="both", expand=True)

    def ver_reportes(self):
        self.limpiar_contenido()
        frame = ReporteFrame(self.contenido)
        frame.pack(fill="both", expand=True)