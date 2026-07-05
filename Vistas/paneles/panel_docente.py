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
from Vistas.ui.shell import DashboardShell


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
        root: tk.Tk | None = None,
    ) -> None:
        super().__init__(parent, style="App.TFrame")
        self.contenedor = contenedor
        self.usuario = usuario
        self.on_logout = on_logout

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self._shell = DashboardShell(
            self,
            titulo="Sistema de nivelación uleam",
            usuario=usuario.cedula,
            rol="Docente",
            menu_titulo="ADMINISTRACIÓN",
            on_logout=on_logout,
            root=root,
        )
        self._shell.grid(row=0, column=0, sticky="nsew")

        self._opciones = [
            ("Estudiantes", self._estudiantes),
            ("Materias", self._materias),
            ("Calificaciones", self._calificaciones),
            ("Aulas", self._aulas),
            ("Cursos", self._cursos),
            ("Postulantes", self._postulantes),
            ("Matrículas", self._matriculas),
            ("Reportes", self._reportes),
        ]
        for i, (texto, cmd) in enumerate(self._opciones):
            self._shell.sidebar.agregar_item(texto, lambda c=cmd, idx=i: self._navegar(c, idx))

        self._navegar(self._estudiantes, 0)

    def _navegar(self, comando: Callable[[], None], indice: int) -> None:
        self._shell.sidebar.marcar(indice)
        comando()

    def _limpiar(self) -> None:
        self._shell.limpiar_contenido()

    def _estudiantes(self) -> None:
        self._limpiar()
        EstudiantesFrame(self._shell.contenido, self.contenedor.gestor).grid(row=0, column=0, sticky="nsew")

    def _materias(self) -> None:
        self._limpiar()
        MateriasFrame(self._shell.contenido, self.contenedor.gestor).grid(row=0, column=0, sticky="nsew")

    def _calificaciones(self) -> None:
        self._limpiar()
        CalificacionesFrame(self._shell.contenido, self.contenedor.gestor).grid(row=0, column=0, sticky="nsew")

    def _aulas(self) -> None:
        self._limpiar()
        CrudJsonFrame(
            self._shell.contenido, "Gestión de Aulas", "aulas", ["codigo", "capacidad"], ["id", "codigo", "capacidad"]
        ).grid(row=0, column=0, sticky="nsew")

    def _cursos(self) -> None:
        self._limpiar()
        CrudJsonFrame(
            self._shell.contenido,
            "Gestión de Cursos",
            "cursos",
            ["nombre", "carrera", "cupos"],
            ["id", "nombre", "carrera", "cupos"],
        ).grid(row=0, column=0, sticky="nsew")

    def _postulantes(self) -> None:
        self._limpiar()
        CrudJsonFrame(
            self._shell.contenido,
            "Gestión de Postulantes",
            "postulantes",
            ["nombre", "cedula", "carrera", "puntaje", "correo"],
            ["id", "nombre", "cedula", "carrera", "puntaje", "correo"],
        ).grid(row=0, column=0, sticky="nsew")

    def _matriculas(self) -> None:
        self._limpiar()
        MatriculaFrame(self._shell.contenido, self.contenedor.gestor, self.contenedor.matricula).grid(
            row=0, column=0, sticky="nsew"
        )

    def _reportes(self) -> None:
        self._limpiar()
        ReporteFrame(self._shell.contenido, self.contenedor.matricula).grid(row=0, column=0, sticky="nsew")
