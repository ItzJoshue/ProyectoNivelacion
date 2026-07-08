import tkinter as tk
from tkinter import ttk
from typing import Callable

from domain.entidades.usuario import Usuario
from servicios.contenedor import ContenedorAplicacion, crear_contenedor
from Vistas.autenticacion.login_frame import LoginFrame
from Vistas.autenticacion.registro_frame import RegistroFrame
from Vistas.paneles.panel_docente import PanelDocente
from Vistas.paneles.panel_estudiante import PanelEstudiante
from Vistas.ui.theme import aplicar_tema, TITULO_APP


class App:
    """
    Orquestador de la interfaz gráfica.

    Flujo:
    1. Login / Registro
    2. Según rol → PanelDocente (acceso completo) o PanelEstudiante (vista limitada)

    El contenedor (Facade) se crea una sola vez (Composition Root).
    """

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title(TITULO_APP)
        self.root.geometry("1280x820")
        self.root.minsize(1024, 680)
        aplicar_tema(self.root)

        self.contenedor: ContenedorAplicacion = crear_contenedor()
        self.usuario_actual: Usuario | None = None

        self._contenedor_vistas = ttk.Frame(root, style="App.TFrame")
        self._contenedor_vistas.pack(fill=tk.BOTH, expand=True)
        self._contenedor_vistas.columnconfigure(0, weight=1)
        self._contenedor_vistas.rowconfigure(0, weight=1)

        self._mostrar_login()

    def _limpiar_vistas(self) -> None:
        """Remueve de forma segura todos los elementos del contenedor visual."""
        for widget in self._contenedor_vistas.winfo_children():
            widget.destroy()

    def _mostrar_login(self) -> None:
        """Carga el formulario de inicio de sesión."""
        self._limpiar_vistas()
        self.usuario_actual = None
        self.root.title(f"{TITULO_APP} — Iniciar sesión")

        login = LoginFrame(
            self._contenedor_vistas,
            self.contenedor,
            on_login=self._entrar,
            on_registro=self._mostrar_registro,
        )
        login.grid(row=0, column=0, sticky="nsew")

    def _mostrar_registro(self) -> None:
        """Carga el formulario de registro de nuevos usuarios."""
        self._limpiar_vistas()
        self.root.title(f"{TITULO_APP} — Registro")

        registro = RegistroFrame(
            self._contenedor_vistas,
            self.contenedor,
            on_registrado=self._mostrar_login,
            on_volver=self._mostrar_login,
        )
        registro.grid(row=0, column=0, sticky="nsew", padx=48, pady=32)

    def _entrar(self, usuario: Usuario) -> None:
        """
        STRATEGY (patrón de comportamiento): selecciona el panel según el rol.
        PanelDocente y PanelEstudiante son estrategias intercambiables de interfaz.
        """
        self.usuario_actual = usuario
        self._limpiar_vistas()
        self.root.title(f"{TITULO_APP} — {usuario.rol.capitalize()}")

        # Despacho dinámico (Strategy Pattern) estructurado limpiamente
        estrategias_paneles = {
            "docente": PanelDocente,
            "estudiante": PanelEstudiante
        }

        constructor_panel = estrategias_paneles.get(usuario.rol.lower())
        if constructor_panel:
            panel = constructor_panel(
                self._contenedor_vistas,
                self.contenedor,
                usuario,
                on_logout=self._mostrar_login,
                root=self.root,
            )
            panel.grid(row=0, column=0, sticky="nsew")
