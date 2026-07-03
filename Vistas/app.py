import tkinter as tk
from tkinter import ttk

from domain.entidades.usuario import Usuario
from servicios.contenedor import ContenedorAplicacion, crear_contenedor
from Vistas.autenticacion.login_frame import LoginFrame
from Vistas.autenticacion.registro_frame import RegistroFrame
from Vistas.paneles.panel_docente import PanelDocente
from Vistas.paneles.panel_estudiante import PanelEstudiante


class App:
    """
    Orquestador de la interfaz gráfica.

    Flujo:
    1. Login / Registro
    2. Según rol → PanelDocente (acceso completo) o PanelEstudiante (vista limitada)

    El contenedor de dependencias se crea una sola vez (Composition Root).
    """

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("ULEAM Management System - Nivelación")
        self.root.geometry("1100x720")
        self.root.minsize(900, 600)

        # INYECCIÓN DE DEPENDENCIAS: todos los servicios vienen del contenedor
        self.contenedor: ContenedorAplicacion = crear_contenedor()
        self.usuario_actual: Usuario | None = None

        self._contenedor_vistas = ttk.Frame(root)
        self._contenedor_vistas.pack(fill=tk.BOTH, expand=True)

        self._mostrar_login()

    def _limpiar_vistas(self) -> None:
        for widget in self._contenedor_vistas.winfo_children():
            widget.destroy()

    def _mostrar_login(self) -> None:
        self._limpiar_vistas()
        self.usuario_actual = None
        self.root.title("ULEAM - Iniciar sesión")
        login = LoginFrame(
            self._contenedor_vistas,
            self.contenedor.autenticacion,
            on_login=self._entrar,
            on_registro=self._mostrar_registro,
        )
        login.place(relx=0.5, rely=0.45, anchor=tk.CENTER)

    def _mostrar_registro(self) -> None:
        self._limpiar_vistas()
        self.root.title("ULEAM - Registro")
        registro = RegistroFrame(
            self._contenedor_vistas,
            self.contenedor.autenticacion,
            on_registrado=self._mostrar_login,
            on_volver=self._mostrar_login,
        )
        registro.pack(fill=tk.BOTH, expand=True, padx=40, pady=30)

    def _entrar(self, usuario: Usuario) -> None:
        self.usuario_actual = usuario
        self._limpiar_vistas()
        self.root.title(f"ULEAM - {usuario.rol.capitalize()}")

        # CONTROL DE ACCESO POR ROL (polimorfismo de vistas)
        if usuario.rol == "docente":
            PanelDocente(
                self._contenedor_vistas,
                self.contenedor,
                usuario,
                on_logout=self._mostrar_login,
            ).pack(fill=tk.BOTH, expand=True)
        else:
            PanelEstudiante(
                self._contenedor_vistas,
                self.contenedor,
                usuario,
                on_logout=self._mostrar_login,
            ).pack(fill=tk.BOTH, expand=True)
