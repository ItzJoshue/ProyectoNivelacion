import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from Utilidades.almacenamiento import leer_json, guardar_json, nuevo_id

class CrudFrame(tk.Frame):
    def __init__(self, parent, titulo, archivo, campos, columnas):
        super().__init__(parent, bg="#eaf6ff")
        self.archivo = archivo
        self.campos = campos
        self.columnas = columnas
        self.vars = {}
        self.id_seleccionado = None

        tk.Label(
            self, text=titulo, bg="#eaf6ff", fg="black",
            font=("Arial", 18, "bold")
        ).pack(anchor="w", pady=(0, 12))

        formulario = tk.Frame(self, bg="white", padx=10, pady=8)
        formulario.pack(fill="x")

        for i, campo in enumerate(campos):
            fila = i // 2
            col = (i % 2) * 2

            tk.Label(formulario, text=campo.capitalize(), bg="white", fg="black").grid(
                row=fila, column=col, sticky="w", padx=6, pady=6
            )

            var = tk.StringVar()
            entrada = tk.Entry(formulario, textvariable=var, width=42)
            entrada.grid(row=fila, column=col + 1, sticky="ew", padx=6, pady=6)
            self.vars[campo] = var

        botones = tk.Frame(self, bg="#eaf6ff")
        botones.pack(fill="x", pady=10)

        tk.Button(botones, text="Guardar", width=14, command=self.guardar).pack(side="left", padx=4)
        tk.Button(botones, text="Actualizar", width=14, command=self.actualizar).pack(side="left", padx=4)
        tk.Button(botones, text="Eliminar", width=14, command=self.eliminar).pack(side="left", padx=4)
        tk.Button(botones, text="Limpiar", width=14, command=self.limpiar).pack(side="left", padx=4)

        marco_tabla = tk.Frame(self, bg="white")
        marco_tabla.pack(fill="both", expand=True)

        self.tabla = ttk.Treeview(marco_tabla, columns=columnas, show="headings")
        scroll_y = ttk.Scrollbar(marco_tabla, orient="vertical", command=self.tabla.yview)
        scroll_x = ttk.Scrollbar(marco_tabla, orient="horizontal", command=self.tabla.xview)

        self.tabla.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

        for col in columnas:
            self.tabla.heading(col, text=col.upper())
            self.tabla.column(col, width=145, anchor="center")

        self.tabla.grid(row=0, column=0, sticky="nsew")
        scroll_y.grid(row=0, column=1, sticky="ns")
        scroll_x.grid(row=1, column=0, sticky="ew")

        marco_tabla.rowconfigure(0, weight=1)
        marco_tabla.columnconfigure(0, weight=1)

        self.tabla.bind("<<TreeviewSelect>>", self.cargar_seleccion)
        self.refrescar()

    def validar(self):
        for campo, var in self.vars.items():
            if not var.get().strip():
                messagebox.showwarning("Validación", f"El campo '{campo}' es obligatorio.")
                return False

        if self.archivo == "aulas":
            try:
                if int(self.vars["capacidad"].get()) <= 0:
                    raise ValueError
            except Exception:
                messagebox.showwarning("Validación", "La capacidad debe ser un número mayor a 0.")
                return False

        if self.archivo == "cursos":
            try:
                if int(self.vars["cupos"].get()) <= 0:
                    raise ValueError
            except Exception:
                messagebox.showwarning("Validación", "Los cupos deben ser un número mayor a 0.")
                return False

        if self.archivo == "postulantes":
            try:
                if float(self.vars["puntaje"].get()) < 0:
                    raise ValueError
            except Exception:
                messagebox.showwarning("Validación", "El puntaje debe ser un número válido.")
                return False

        return True

    def guardar(self):
        if not self.validar():
            return

        datos = leer_json(self.archivo)

        if "cedula" in self.vars:
            cedula = self.vars["cedula"].get().strip()
            if any(item.get("cedula") == cedula for item in datos):
                messagebox.showwarning("Duplicado", "Ya existe un registro con esa cédula.")
                return

        if "codigo" in self.vars:
            codigo = self.vars["codigo"].get().strip()
            if any(item.get("codigo") == codigo for item in datos):
                messagebox.showwarning("Duplicado", "Ya existe un aula con ese código.")
                return

        nuevo = {"id": nuevo_id(self.archivo[:3].upper())}
        for campo, var in self.vars.items():
            nuevo[campo] = var.get().strip()

        datos.append(nuevo)

        if guardar_json(self.archivo, datos):
            self.refrescar()
            self.limpiar()
            messagebox.showinfo("Correcto", "Registro guardado correctamente.")

    def actualizar(self):
        if not self.id_seleccionado:
            messagebox.showwarning("Aviso", "Primero selecciona un registro.")
            return

        if not self.validar():
            return

        datos = leer_json(self.archivo)

        for item in datos:
            if item.get("id") == self.id_seleccionado:
                for campo, var in self.vars.items():
                    item[campo] = var.get().strip()

        if guardar_json(self.archivo, datos):
            self.refrescar()
            self.limpiar()
            messagebox.showinfo("Correcto", "Registro actualizado correctamente.")

    def eliminar(self):
        if not self.id_seleccionado:
            messagebox.showwarning("Aviso", "Primero selecciona un registro.")
            return

        if not messagebox.askyesno("Confirmar", "¿Seguro que deseas eliminar este registro?"):
            return

        datos = leer_json(self.archivo)
        datos = [item for item in datos if item.get("id") != self.id_seleccionado]

        if guardar_json(self.archivo, datos):
            self.refrescar()
            self.limpiar()
            messagebox.showinfo("Correcto", "Registro eliminado correctamente.")

    def limpiar(self):
        self.id_seleccionado = None
        for var in self.vars.values():
            var.set("")
        for sel in self.tabla.selection():
            self.tabla.selection_remove(sel)

    def refrescar(self):
        for item in self.tabla.get_children():
            self.tabla.delete(item)

        for registro in leer_json(self.archivo):
            valores = [registro.get(col, "") for col in self.columnas]
            self.tabla.insert("", "end", values=valores)

    def cargar_seleccion(self, event=None):
        seleccion = self.tabla.selection()
        if not seleccion:
            return

        valores = self.tabla.item(seleccion[0], "values")
        if not valores:
            return

        self.id_seleccionado = valores[0]
        datos = leer_json(self.archivo)

        registro = next((item for item in datos if item.get("id") == self.id_seleccionado), None)

        if registro:
            for campo in self.campos:
                self.vars[campo].set(registro.get(campo, ""))