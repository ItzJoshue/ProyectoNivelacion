import tkinter as tk
from tkinter import messagebox, ttk

from infraestructura.utilidades.almacenamiento import DATA_DIR
from servicios.matricula_servicio import MatriculaServicio


class ReporteFrame(ttk.Frame):
    def __init__(self, parent: tk.Widget, matricula: MatriculaServicio) -> None:
        super().__init__(parent, padding=10)
        self.matricula = matricula
        ttk.Label(self, text="Reportes", font=("Segoe UI", 14, "bold")).pack(anchor=tk.W, pady=(0, 10))
        btns = ttk.Frame(self)
        btns.pack(fill=tk.X)
        ttk.Button(btns, text="Generar reporte", command=self._generar).pack(side=tk.LEFT, padx=4)
        ttk.Button(btns, text="Ver carpeta de datos", command=self._ruta).pack(side=tk.LEFT, padx=4)
        self.texto = tk.Text(self, height=22, wrap=tk.WORD)
        self.texto.pack(fill=tk.BOTH, expand=True, pady=8)

    def _generar(self) -> None:
        self.texto.delete("1.0", tk.END)
        self.texto.insert(tk.END, self.matricula.generar_reporte())

    def _ruta(self) -> None:
        messagebox.showinfo("Datos", f"Los archivos JSON están en:\n{DATA_DIR}")
