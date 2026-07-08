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
from Vistas.ui.theme import TITULO_APP


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
            titulo=TITULO_APP,
            usuario=usuario.cedula,
            rol="Docente",
            menu_titulo="ADMINISTRACIÓN",
            on_logout=on_logout,
            root=root,
        )
        self._shell.grid(row=0, column=0, sticky="nsew")

        # Estrategia OCP: Mapeo unificado de componentes de infraestructura visual.
        # Esto permite registrar o quitar vistas modificando solo este diccionario.
        self._vistas_registro = {
            "Estudiantes": lambda: EstudiantesFrame(self._shell.contenido, self.contenedor),
            "Materias": lambda: MateriasFrame(self._shell.contenido, self.contenedor),
            "Calificaciones": lambda: CalificacionesFrame(self._shell.contenido, self.contenedor),
            "Aulas": lambda: CrudJsonFrame(
                self._shell.contenido, "Gestión de Aulas", "aulas", ["codigo", "capacidad"], ["id", "codigo", "capacidad"]
            ),
            "Cursos": lambda: CrudJsonFrame(
                self._shell.contenido, "Gestión de Cursos", "cursos", ["nombre", "carrera", "cupos"], ["id", "nombre", "carrera", "cupos"]
            ),
            "Postulantes": lambda: CrudJsonFrame(
                self._shell.contenido, "Gestión de Postulantes", "postulantes", ["nombre", "cedula", "carrera", "puntaje", "correo"], ["id", "nombre", "cedula", "carrera", "puntaje", "correo"]
            ),
            "Matrículas": lambda: MatriculaFrame(self._shell.contenido, self.contenedor),
            "Reportes": lambda: ReporteFrame(self._shell.contenido, self.contenedor),
        }

        # Construcción dinámica de la Sidebar
        for indice, nombre_pestana in enumerate(self._vistas_registro.keys()):
            self._shell.sidebar.agregar_item(
                nombre_pestana, 
                lambda n=nombre_pestana, idx=indice: self._navegar_a(n, idx)
            )

        # Carga por defecto de la primera vista del sistema
        self._navegar_a("Estudiantes", 0)

    def _navegar_a(self, nombre_vista: str, indice: int) -> None:
        """Despachador dinámico que cumple con SRP al centralizar la navegación."""
        self._shell.sidebar.marcar(indice)
        self._shell.limpiar_contenido()
        
        # Factory implícito: invoca la función lambda correspondiente al nombre
        constructor_vista = self._vistas_registro.get(nombre_vista)
        if constructor_vista:
            instancia_vista = constructor_vista()
            instancia_vista.grid(row=0, column=0, sticky="nsew")
