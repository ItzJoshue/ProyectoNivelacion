import tkinter as tk
from tkinter import messagebox, ttk
from typing import Callable

from servicios.autenticacion_servicio import AutenticacionServicio
from Vistas.ui.components import Card, SPACE_MD, button_row, form_field, page_header


class RegistroFrame(ttk.Frame):
    """Registro de cuenta como estudiante o docente."""

    _CAMPOS_COMUNES = [
        ("Cédula", "cedula"),
        ("Nombre", "nombre"),
        ("Apellido", "apellido"),
    ]
    _CAMPOS_ESTUDIANTE = [
        ("Carrera", "carrera"),
        ("Email", "email"),
    ]
    _CAMPOS_DOCENTE = [
        ("Departamento", "departamento"),
    ]
    _CAMPOS_CREDENCIALES = [
        ("Contraseña", "contrasena"),
        ("Confirmar contraseña", "confirmar"),
    ]

    def __init__(
        self,
        parent: tk.Widget,
        auth: AutenticacionServicio,
        on_registrado: Callable[[], None],
        on_volver: Callable[[], None],
    ) -> None:
        super().__init__(parent, style="App.TFrame")
        self.auth = auth
        self.on_registrado = on_registrado
        self.on_volver = on_volver

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        scroll_host = ttk.Frame(self, style="App.TFrame")
        scroll_host.grid(row=0, column=0, sticky="nsew")
        scroll_host.columnconfigure(0, weight=1)

        page_header(scroll_host, "Crear cuenta", "Complete sus datos para registrarse en el sistema").pack(
            fill=tk.X, pady=(0, SPACE_MD)
        )

        layout = ttk.Frame(scroll_host, style="App.TFrame")
        layout.pack(fill=tk.BOTH, expand=True)
        layout.columnconfigure(0, weight=1)
        layout.columnconfigure(1, weight=1)

        self.var_rol = tk.StringVar(value="estudiante")
        self.vars = {
            "cedula": tk.StringVar(),
            "nombre": tk.StringVar(),
            "apellido": tk.StringVar(),
            "carrera": tk.StringVar(),
            "departamento": tk.StringVar(),
            "email": tk.StringVar(),
            "contrasena": tk.StringVar(),
            "confirmar": tk.StringVar(),
        }

        card = Card(layout, title="Datos del estudiante")
        card.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, SPACE_MD))
        self._card = card

        rol_box = ttk.Frame(card.body, style="Card.TFrame")
        rol_box.pack(fill=tk.X, pady=(0, SPACE_MD))
        ttk.Label(rol_box, text="Registrarme como", style="Field.TLabel").pack(anchor=tk.W)
        rol_btns = ttk.Frame(rol_box, style="Card.TFrame")
        rol_btns.pack(anchor=tk.W, pady=(4, 0))
        ttk.Radiobutton(
            rol_btns, text="Estudiante", variable=self.var_rol, value="estudiante",
            style="Modern.TRadiobutton", command=self._actualizar_campos_rol,
        ).pack(side=tk.LEFT, padx=(0, 16))
        ttk.Radiobutton(
            rol_btns, text="Docente", variable=self.var_rol, value="docente",
            style="Modern.TRadiobutton", command=self._actualizar_campos_rol,
        ).pack(side=tk.LEFT)

        self._form = ttk.Frame(card.body, style="Card.TFrame")
        self._form.pack(fill=tk.X)
        self._form.columnconfigure(0, weight=1)
        self._form.columnconfigure(1, weight=1)

        self._widgets: dict[str, tuple[ttk.Frame, ttk.Entry]] = {}
        for etiqueta, clave in (
            self._CAMPOS_COMUNES + self._CAMPOS_ESTUDIANTE + self._CAMPOS_DOCENTE + self._CAMPOS_CREDENCIALES
        ):
            show = "*" if clave in ("contrasena", "confirmar") else None
            self._widgets[clave] = form_field(self._form, etiqueta, self.vars[clave], show=show, width=32)

        acciones = ttk.Frame(layout, style="App.TFrame")
        acciones.grid(row=1, column=0, columnspan=2, sticky="w")
        button_row(
            acciones,
            [
                ("Registrar", self._registrar, "primary"),
                ("Volver al login", self.on_volver, "secondary"),
            ],
        ).pack(anchor=tk.W)

        self._actualizar_campos_rol()

    def _actualizar_campos_rol(self) -> None:
        es_estudiante = self.var_rol.get() == "estudiante"
        visibles = (
            [c for _, c in self._CAMPOS_COMUNES]
            + ([c for _, c in self._CAMPOS_ESTUDIANTE] if es_estudiante else [c for _, c in self._CAMPOS_DOCENTE])
            + [c for _, c in self._CAMPOS_CREDENCIALES]
        )

        if es_estudiante:
            self.vars["departamento"].set("")
        else:
            self.vars["carrera"].set("")
            self.vars["email"].set("")

        col = 0
        row = 0
        for clave, (container, _) in self._widgets.items():
            if clave in visibles:
                container.grid(row=row, column=col, sticky="ew", padx=(0, 12) if col == 0 else (12, 0))
                col += 1
                if col > 1:
                    col = 0
                    row += 1
            else:
                container.grid_remove()

        self._card.set_title("Datos del estudiante" if es_estudiante else "Datos del docente")

    def _registrar(self) -> None:
        if self.vars["contrasena"].get() != self.vars["confirmar"].get():
            messagebox.showwarning("Validación", "Las contraseñas no coinciden.")
            return

        rol = self.var_rol.get()
        datos = {
            "cedula": self.vars["cedula"].get().strip(),
            "nombre": self.vars["nombre"].get().strip(),
            "apellido": self.vars["apellido"].get().strip(),
        }

        if rol == "estudiante":
            datos["carrera"] = self.vars["carrera"].get().strip()
            datos["email"] = self.vars["email"].get().strip()
        else:
            datos["departamento"] = self.vars["departamento"].get().strip()

        try:
            self.auth.registrar(datos, self.vars["contrasena"].get(), rol)
            messagebox.showinfo("Éxito", f"Cuenta de {rol} creada. Ya puede iniciar sesión.")
            self.on_registrado()
        except ValueError as error:
            messagebox.showerror("Error", str(error))
