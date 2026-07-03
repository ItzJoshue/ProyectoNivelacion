import tkinter as tk
from tkinter import ttk
from typing import Callable

from domain.entidades.usuario import Usuario
from servicios.contenedor import ContenedorAplicacion
from Vistas.frames.mi_perfil_frame import MiPerfilFrame
from Vistas.frames.mis_calificaciones_frame import MisCalificacionesFrame


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
    ) -> None:
        super().__init__(parent)
        self.contenedor = contenedor
        self.usuario = usuario
        self.on_logout = on_logout

        header = ttk.Frame(self, padding=(12, 8))
        header.pack(fill=tk.X)
        ttk.Label(
            header,
            text=f"Panel Estudiante — {usuario.cedula}",
            font=("Segoe UI", 14, "bold"),
        ).pack(side=tk.LEFT)
        ttk.Button(header, text="Cerrar sesión", command=on_logout).pack(side=tk.RIGHT)

        cuerpo = ttk.Frame(self)
        cuerpo.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

        menu = ttk.Frame(cuerpo, width=160)
        menu.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        menu.pack_propagate(False)

        self.contenido = ttk.Frame(cuerpo)
        self.contenido.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        ttk.Button(menu, text="Mi perfil", command=self._perfil, width=16).pack(pady=4, fill=tk.X)
        ttk.Button(menu, text="Mis calificaciones", command=self._calificaciones, width=16).pack(
            pady=4, fill=tk.X
        )

        self._perfil()

    def _limpiar(self) -> None:
        for w in self.contenido.winfo_children():
            w.destroy()

    def _perfil(self) -> None:
        self._limpiar()
        MiPerfilFrame(
            self.contenido,
            self.usuario.cedula,
            self.contenedor.autenticacion,
            self.contenedor.matricula,
        ).pack(fill=tk.BOTH, expand=True)

    def _calificaciones(self) -> None:
        self._limpiar()
        MisCalificacionesFrame(
            self.contenido,
            self.usuario.cedula,
            self.contenedor.autenticacion,
            self.contenedor.matricula,
        ).pack(fill=tk.BOTH, expand=True)
