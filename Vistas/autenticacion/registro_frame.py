import tkinter as tk
from tkinter import messagebox, ttk
from typing import Callable

from servicios.autenticacion_servicio import AutenticacionServicio


class RegistroFrame(ttk.Frame):
    """Registro de cuenta como estudiante o docente."""

    def __init__(
        self,
        parent: tk.Widget,
        auth: AutenticacionServicio,
        on_registrado: Callable[[], None],
        on_volver: Callable[[], None],
    ) -> None:
        super().__init__(parent, padding=20)
        self.auth = auth
        self.on_registrado = on_registrado
        self.on_volver = on_volver

        ttk.Label(self, text="Crear cuenta", font=("Segoe UI", 16, "bold")).pack(anchor=tk.W, pady=(0, 12))

        form = ttk.LabelFrame(self, text="Datos personales", padding=12)
        form.pack(fill=tk.X, pady=(0, 10))

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

        ttk.Label(form, text="Registrarme como:").grid(row=0, column=0, sticky=tk.W, pady=4)
        rol_frame = ttk.Frame(form)
        rol_frame.grid(row=0, column=1, sticky=tk.W, pady=4)
        ttk.Radiobutton(
            rol_frame, text="Estudiante", variable=self.var_rol, value="estudiante"
        ).pack(side=tk.LEFT, padx=(0, 12))
        ttk.Radiobutton(rol_frame, text="Docente", variable=self.var_rol, value="docente").pack(
            side=tk.LEFT
        )

        campos = [
            ("Cédula:", "cedula"),
            ("Nombre:", "nombre"),
            ("Apellido:", "apellido"),
            ("Carrera (estudiante):", "carrera"),
            ("Departamento (docente):", "departamento"),
            ("Email:", "email"),
            ("Contraseña:", "contrasena"),
            ("Confirmar contraseña:", "confirmar"),
        ]

        for i, (etiqueta, clave) in enumerate(campos, start=1):
            ttk.Label(form, text=etiqueta).grid(row=i, column=0, sticky=tk.W, pady=3)
            show = "*" if "contrasena" in clave or clave == "confirmar" else None
            ttk.Entry(form, textvariable=self.vars[clave], width=36, show=show).grid(
                row=i, column=1, sticky=tk.W, padx=8, pady=3
            )

        btns = ttk.Frame(self)
        btns.pack(pady=12)
        ttk.Button(btns, text="Registrar", command=self._registrar).pack(side=tk.LEFT, padx=6)
        ttk.Button(btns, text="Volver al login", command=self.on_volver).pack(side=tk.LEFT, padx=6)

    def _registrar(self) -> None:
        if self.vars["contrasena"].get() != self.vars["confirmar"].get():
            messagebox.showwarning("Validación", "Las contraseñas no coinciden.")
            return

        rol = self.var_rol.get()
        datos = {
            "cedula": self.vars["cedula"].get().strip(),
            "nombre": self.vars["nombre"].get().strip(),
            "apellido": self.vars["apellido"].get().strip(),
            "carrera": self.vars["carrera"].get().strip(),
            "departamento": self.vars["departamento"].get().strip(),
            "email": self.vars["email"].get().strip(),
        }

        try:
            self.auth.registrar(datos, self.vars["contrasena"].get(), rol)
            messagebox.showinfo("Éxito", f"Cuenta de {rol} creada. Ya puede iniciar sesión.")
            self.on_registrado()
        except ValueError as error:
            messagebox.showerror("Error", str(error))
