import json
import uuid
from pathlib import Path
from tkinter import messagebox

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "Datos"
DATA_DIR.mkdir(parents=True, exist_ok=True)

ARCHIVOS = {
    "estudiantes": DATA_DIR / "estudiantes.json",
    "profesores": DATA_DIR / "profesores.json",
    "aulas": DATA_DIR / "aulas.json",
    "cursos": DATA_DIR / "cursos.json",
    "postulantes": DATA_DIR / "postulantes.json",
    "matriculas": DATA_DIR / "matriculas.json",
}

def iniciar_json():
    for ruta in ARCHIVOS.values():
        ruta.parent.mkdir(parents=True, exist_ok=True)
        if not ruta.exists():
            ruta.write_text("[]", encoding="utf-8")

def leer_json(nombre):
    ruta = ARCHIVOS[nombre]
    try:
        if not ruta.exists():
            ruta.write_text("[]", encoding="utf-8")

        texto = ruta.read_text(encoding="utf-8").strip()
        if not texto:
            return []

        datos = json.loads(texto)
        return datos if isinstance(datos, list) else []
    except json.JSONDecodeError:
        ruta.write_text("[]", encoding="utf-8")
        messagebox.showwarning("JSON reiniciado", f"El archivo {ruta.name} estaba dañado y fue reiniciado.")
        return []
    except Exception as e:
        messagebox.showerror("Error de lectura", f"No se pudo leer:\n{ruta}\n\n{e}")
        return []

def guardar_json(nombre, datos):
    ruta = ARCHIVOS[nombre]
    try:
        ruta.parent.mkdir(parents=True, exist_ok=True)
        with open(ruta, "w", encoding="utf-8") as archivo:
            json.dump(datos, archivo, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        messagebox.showerror("Error de guardado", f"No se pudo guardar:\n{ruta}\n\n{e}")
        return False

def nuevo_id(prefijo):
    return f"{prefijo}-{uuid.uuid4().hex[:6].upper()}"