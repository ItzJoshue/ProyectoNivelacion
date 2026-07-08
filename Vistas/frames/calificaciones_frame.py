import tkinter as tk
from tkinter import messagebox, ttk

from servicios.contenedor import ContenedorAplicacion
from Vistas.ui.components import Card, SPACE_MD, button_row, form_field, page_header, styled_text


class CalificacionesFrame(ttk.Frame):
     """Gestiona el registro y consulta de calificaciones académicas.
        Permite asociar calificaciones a estudiantes y materias, así como
        visualizar información relacionada con el rendimiento académico
        dentro del sistema de gestión académica."""
    def __init__(self, parent: tk.Widget, contenedor: ContenedorAplicacion) -> None:
        super().__init__(parent, style="Content.TFrame")
        self.contenedor = contenedor
        self.var_cedula = tk.StringVar()
        self.var_materia = tk.StringVar()
        self.var_nota = tk.StringVar()

        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)

        page_header(self, "Calificaciones", "Registre notas y consulte el rendimiento académico").grid(
            row=0, column=0, sticky="ew"
        )

        form_card = Card(self, title="Registrar calificación")
        form_card.grid(row=1, column=0, sticky="ew", pady=(0, SPACE_MD))
        form_card.body.columnconfigure(0, weight=1)
        form_card.body.columnconfigure(1, weight=1)
        form_card.body.columnconfigure(2, weight=1)

        cedula_frame, _ = form_field(
            form_card.body,
            "Cédula del estudiante",
            self.var_cedula,
            width=22
        )
        cedula_frame.grid(row=0, column=0, sticky="ew", padx=(0, 8))

        materia_frame, _ = form_field(
            form_card.body,
            "Materia",
            self.var_materia,
            width=22
        )
        materia_frame.grid(row=0, column=1, sticky="ew", padx=8)

        nota_frame, _ = form_field(
            form_card.body,
            "Nota (0-10)",
            self.var_nota,
            width=22
        )
        nota_frame.grid(row=0, column=2, sticky="ew", padx=(8, 0))

        acciones = ttk.Frame(form_card.body, style="Card.TFrame")
        acciones.grid(row=1, column=0, columnspan=3, sticky="w", pady=(4, 0))
        button_row(acciones, [("Guardar calificación", self._guardar, "primary")]).pack(anchor=tk.W)

        resumen_card = Card(self, title="Resumen de estudiantes")
        resumen_card.grid(row=2, column=0, sticky="nsew")
        resumen_card.body.rowconfigure(0, weight=1)
        resumen_card.body.columnconfigure(0, weight=1)

        texto_wrap = ttk.Frame(resumen_card.body, style="Card.TFrame")
        texto_wrap.grid(row=0, column=0, sticky="nsew")
        texto_wrap.rowconfigure(0, weight=1)
        texto_wrap.columnconfigure(0, weight=1)

        self.texto = styled_text(texto_wrap, height=20, wrap=tk.WORD)
        self.texto.grid(row=0, column=0, sticky="nsew")

        vsb = ttk.Scrollbar(texto_wrap, orient=tk.VERTICAL, command=self.texto.yview, style="Modern.Vertical.TScrollbar")
        self.texto.configure(yscrollcommand=vsb.set)
        vsb.grid(row=0, column=1, sticky="ns")
        self.refrescar()

    def refrescar(self) -> None:
        """Actualiza el resumen de estudiantes mostrado en pantalla.
           Obtiene la información desde el gestor académico y reconstruye
           el contenido del área de texto para reflejar los datos actuales."""
        self.texto.config(state=tk.NORMAL)
        self.texto.delete("1.0", tk.END)
        estudiantes = self.contenedor.gestor.listar_estudiantes()
        if not estudiantes:
            self.texto.insert(tk.END, "No hay estudiantes registrados.\n")
        else:
            for resumen in self.contenedor.gestor.obtener_resumenes_personas(estudiantes):
                self.texto.insert(tk.END, f"• {resumen}\n")
        self.texto.config(state=tk.DISABLED)

    def _guardar(self) -> None:
        """Registra una nueva calificación para un estudiante.
           La interfaz recopila los datos ingresados por el usuario y delega
           la validación y almacenamiento al gestor académico, manteniendo
           separadas las responsabilidades de presentación y lógica de negocio."""
        try:
            self.contenedor.gestor.registrar_calificacion(
                self.var_cedula.get().strip(),
                self.var_materia.get().strip(),
                float(self.var_nota.get()),
            )
            self.var_nota.set("")
            self.refrescar()
            messagebox.showinfo("Éxito", "Calificación registrada.")
        except (ValueError, KeyError) as e:
            messagebox.showerror("Error", str(e))
