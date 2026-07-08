import tkinter as tk
from tkinter import ttk
from typing import Callable

from domain.entidades.usuario import Usuario
from servicios.contenedor import ContenedorAplicacion
from Vistas.frames.mi_perfil_frame import MiPerfilFrame
from Vistas.frames.mis_calificaciones_frame import MisCalificacionesFrame
from Vistas.ui.shell import DashboardShell
from Vistas.ui.theme import TITULO_APP


class PanelEstudiante(ttk.Frame):
    """
    Panel restringido para estudiantes.
    Solo puede ver su perfil, calificaciones y cursos matriculados (no administra otros registros).
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
            rol="Estudiante",
            menu_titulo="MI CUENTA",
            on_logout=on_logout,
            root=root,
        )
        self._shell.grid(row=0, column=0, sticky="nsew")

        self._opciones = [
            ("Mi perfil", self._perfil),
            ("Mis calificaciones", self._calificaciones),
        ]
        for i, (texto, cmd) in enumerate(self._opciones):
            self._shell.sidebar.agregar_item(texto, lambda c=cmd, idx=i: self._navegar(c, idx))

        self._navegar(self._perfil, 0)

    def _navegar(self, comando: Callable[[], None], indice: int) -> None:
        self._shell.sidebar.marcar(indice)
        comando()

    def _limpiar(self) -> None:
        self._shell.limpiar_contenido()

    def _perfil(self) -> None:
        self._limpiar()
        MiPerfilFrame(
            self._shell.contenido,
            self.usuario.cedula,
            self.contenedor,
        ).grid(row=0, column=0, sticky="nsew")

    def _calificaciones(self) -> None:
        self._limpiar()
        MisCalificacionesFrame(
            self._shell.contenido,
            self.usuario.cedula,
            self.contenedor,
        ).grid(row=0, column=0, sticky="nsew")
