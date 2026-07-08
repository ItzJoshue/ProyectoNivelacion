import tkinter as tk
from tkinter import messagebox, ttk
from typing import Callable

from domain.entidades.usuario import Usuario
from servicios.contenedor import ContenedorAplicacion
from Vistas.ui.colors import Colors
from Vistas.ui.components import Card, SPACE_LG, SPACE_MD, SPACE_XL, form_field
from Vistas.ui.icons import dibujar_logo
from Vistas.ui.theme import SUBTITULO_INSTITUCION, TITULO_APP


class LoginFrame(ttk.Frame):
    """
    Pantalla de inicio de sesión — diseño centrado con tarjeta.
    
    Cumple con SRP al delegar exclusivamente la captura de intenciones visuales 
    y el renderizado estructurado del módulo de autenticación.
    """

    def __init__(
        self,
        parent: tk.Widget,
        contenedor: ContenedorAplicacion,
        on_login: Callable[[Usuario], None],
        on_registro: Callable[[], None],
    ) -> None:
        super().__init__(parent, style="App.TFrame")
        
        # 1. Inyección de dependencias y delegaciones mutables 
        self.contenedor = contenedor
        self.on_login = on_login
        self.on_registro = on_registro

        # 2. Inicialización encapsulada de variables de control de estado 
        self.var_cedula = tk.StringVar()
        self.var_contrasena = tk.StringVar()

        # 3. Orquestación del layout y de los componentes de la vista
        self._configurar_grid_principal()
        self._construir_interfaz_grafica()

    def _configurar_grid_principal(self) -> None:
        """Define las propiedades de redimensionamiento elástico del contenedor."""
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

    def _construir_interfaz_grafica(self) -> None:
        """Abstracción modular que compone las sub-vistas del login."""
        centro = ttk.Frame(self, style="App.TFrame", padding=SPACE_XL)
        centro.grid(row=0, column=0)

        self._renderizar_cabecera_institucional(centro)
        self._renderizar_formulario_tarjeta(centro)

    def _renderizar_cabecera_institucional(self, parent: tk.Widget) -> None:
        """Construye la identidad visual de la cabecera (Logotipo y Títulos)."""
        marca = tk.Frame(parent, bg=Colors.BG_APP)
        marca.pack(pady=(0, SPACE_LG))

        logo = tk.Canvas(marca, width=64, height=64, bg=Colors.BG_APP, highlightthickness=0)
        logo.pack()
        dibujar_logo(logo, 64, bg=Colors.BG_APP)

        ttk.Label(parent, text=TITULO_APP, style="Title.TLabel").pack(pady=(0, SPACE_MD))
        ttk.Label(parent, text=SUBTITULO_INSTITUCION, style="Subtitle.TLabel").pack(pady=(0, SPACE_XL))

    def _renderizar_formulario_tarjeta(self, parent: tk.Widget) -> None:
        """Encapsula los campos de texto y botones dentro de un contenedor Card."""
        card = Card(parent, title="Iniciar sesión")
        card.pack()

        # Inserción de campos de entrada desacoplados
        form_field(card.body, "Cédula", self.var_cedula, width=36)[0].pack(fill=tk.X)
        form_field(card.body, "Contraseña", self.var_contrasena, show="•", width=36)[0].pack(fill=tk.X)

        self._construir_acciones_formulario(card.body)

    def _construir_acciones_formulario(self, parent: tk.Widget) -> None:
        """Monta las acciones interactivas para el envío de peticiones lógicas."""
        btns = ttk.Frame(parent, style="Card.TFrame")
        btns.pack(fill=tk.X, pady=(SPACE_MD, 0))

        # Botón de autenticación principal
        btn_login = ttk.Button(btns, text="Iniciar sesión", style="Primary.TButton", command=self._login)
        btn_login.pack(side=tk.LEFT, padx=(0, SPACE_MD))

        # Botón de redirección hacia el registro
        btn_registro = ttk.Button(btns, text="Crear cuenta", style="Secondary.TButton", command=self.on_registro)
        btn_registro.pack(side=tk.LEFT)

    def _login(self) -> None:
        """
        Manejador de eventos lógicos para el procesamiento del login.
        
        Paso de mensajes (Unidad 1): Comunica de forma segura los valores del estado 
        hacia el Facade de la aplicación y gestiona el control de excepciones.
        """
        cedula_limpia = self.var_cedula.get().strip()
        contrasena_cruda = self.var_contrasena.get()

        try:
            # Delegación del control a la capa de servicios lógicos de la aplicación
            usuario = self.contenedor.iniciar_sesion(cedula_limpia, contrasena_cruda)
            self.on_login(usuario)
            
        except ValueError as error:
            messagebox.showerror("Acceso denegado", str(error))
