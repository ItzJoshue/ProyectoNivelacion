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

        # Estrategia OCP (Unidad 3): Registro dinámico de componentes visuales de cuenta.
        # Permite escalar o quitar opciones modificando solo este diccionario de mapeo.
        self._vistas_registro = {
            "Mi perfil": lambda: MiPerfilFrame(
                self._shell.contenido, self.usuario.cedula, self.contenedor
            ),
            "Mis calificaciones": lambda: MisCalificacionesFrame(
                self._shell.contenido, self.usuario.cedula, self.contenedor
            ),
        }

        # Construcción dinámica 
        for indice, nombre_pestana in enumerate(self._vistas_registro.keys()):
            self._shell.sidebar.agregar_item(
                nombre_pestana,
                lambda n=nombre_pestana, idx=indice: self._navegar_a(n, idx)
            )

        # Carga inicial por defecto de la pestaña de perfil
        self._navegar_a("Mi perfil", 0)

    def _navegar_a(self, nombre_vista: str, indice: int) -> None:
        """Despachador centralizado de vistas que cumple con SRP al desacoplar el control del shell."""
        self._shell.sidebar.marcar(indice)
        self._shell.limpiar_contenido()

        # Invocación segura mediante el mapeo del diccionario
        constructor_vista = self._vistas_registro.get(nombre_vista)
        if constructor_vista:
            instancia_vista = constructor_vista()
            instancia_vista.grid(row=0, column=0, sticky="nsew")
