import tkinter as tk
from tkinter import ttk
from typing import Callable

from domain.entidades.usuario import Usuario
from servicios.contenedor import ContenedorAplicacion
from Vistas.frames.calificaciones_frame import CalificacionesFrame
from Vistas.frames.crud_json_frame import CrudJsonFrame
from Vistas.frames.estudiantes_frame import EstudiantesFrame
from Vistas.frames.matricula_frame import MatriculaFrame
from Vistas.frames.materias_frame import MateriasFrame
from Vistas.frames.reporte_frame import ReporteFrame


class PanelDocente(ttk.Frame):
    """
    Panel con acceso completo para docentes.
    Control de acceso basado en rol: solo usuarios con rol 'docente'.
    """

    def __init__(
        self,
        parent: tk.Widget,
        contenedor: ContenedorAplicacion,
        usuario: Usuario,
        on_logout: Callable[[], None],
    ) -> None:
        super().__init__(parent)
        self.contenedor = contenedor
        self.usuario = usuario
        self.on_logout = on_logout

        header = ttk.Frame(self, padding=(12, 8))
        header.pack(fill=tk.X)
        ttk.Label(
            header,
            text=f"Panel Docente — {usuario.cedula}",
            font=("Segoe UI", 14, "bold"),
        ).pack(side=tk.LEFT)
        ttk.Button(header, text="Cerrar sesión", command=on_logout).pack(side=tk.RIGHT)

        cuerpo = ttk.Frame(self)
        cuerpo.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

        menu = ttk.Frame(cuerpo, width=180)
        menu.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        menu.pack_propagate(False)

        self.contenido = ttk.Frame(cuerpo)
        self.contenido.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        opciones = [
            ("Estudiantes", self._estudiantes),
            ("Materias", self._materias),
            ("Calificaciones", self._calificaciones),
            ("Aulas", self._aulas),
            ("Cursos", self._cursos),
            ("Postulantes", self._postulantes),
            ("Matrículas", self._matriculas),
            ("Reportes", self._reportes),
        ]
        for texto, cmd in opciones:
            ttk.Button(menu, text=texto, command=cmd, width=18).pack(pady=4, fill=tk.X)

        self._estudiantes()

    def _limpiar(self) -> None:
        for w in self.contenido.winfo_children():
            w.destroy()

    def _estudiantes(self) -> None:
        self._limpiar()
        EstudiantesFrame(self.contenido, self.contenedor.gestor).pack(fill=tk.BOTH, expand=True)

    def _materias(self) -> None:
        self._limpiar()
        MateriasFrame(self.contenido, self.contenedor.gestor).pack(fill=tk.BOTH, expand=True)

    def _calificaciones(self) -> None:
        self._limpiar()
        CalificacionesFrame(self.contenido, self.contenedor.gestor).pack(fill=tk.BOTH, expand=True)

    def _aulas(self) -> None:
        self._limpiar()
        CrudJsonFrame(
            self.contenido, "Gestión de Aulas", "aulas", ["codigo", "capacidad"], ["id", "codigo", "capacidad"]
        ).pack(fill=tk.BOTH, expand=True)

    def _cursos(self) -> None:
        self._limpiar()
        CrudJsonFrame(
            self.contenido,
            "Gestión de Cursos",
            "cursos",
            ["nombre", "carrera", "cupos"],
            ["id", "nombre", "carrera", "cupos"],
        ).pack(fill=tk.BOTH, expand=True)

    def _postulantes(self) -> None:
        self._limpiar()
        CrudJsonFrame(
            self.contenido,
            "Gestión de Postulantes",
            "postulantes",
            ["nombre", "cedula", "carrera", "puntaje", "correo"],
            ["id", "nombre", "cedula", "carrera", "puntaje", "correo"],
        ).pack(fill=tk.BOTH, expand=True)

    def _matriculas(self) -> None:
        self._limpiar()
        MatriculaFrame(self.contenido, self.contenedor.gestor, self.contenedor.matricula).pack(
            fill=tk.BOTH, expand=True
        )

    def _reportes(self) -> None:
        self._limpiar()
        ReporteFrame(self.contenido, self.contenedor.matricula).pack(fill=tk.BOTH, expand=True)
