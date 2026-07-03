import json
import uuid
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "Datos"

ARCHIVOS = {
    "estudiantes": DATA_DIR / "estudiantes.json",
    "docentes": DATA_DIR / "docentes.json",
    "profesores": DATA_DIR / "profesores.json",
    "usuarios": DATA_DIR / "usuarios.json",
    "materias": DATA_DIR / "materias.json",
    "aulas": DATA_DIR / "aulas.json",
    "cursos": DATA_DIR / "cursos.json",
    "postulantes": DATA_DIR / "postulantes.json",
    "matriculas": DATA_DIR / "matriculas.json",
}


def iniciar_datos() -> None:
    """Inicializa archivos JSON vacíos (persistencia de la rama Modulosss)."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    for ruta in ARCHIVOS.values():
        if not ruta.exists():
            ruta.write_text("[]", encoding="utf-8")


def leer_json(nombre: str) -> list:
    ruta = ARCHIVOS[nombre]
    iniciar_datos()
    try:
        texto = ruta.read_text(encoding="utf-8").strip()
        if not texto:
            return []
        datos = json.loads(texto)
        return datos if isinstance(datos, list) else []
    except json.JSONDecodeError:
        ruta.write_text("[]", encoding="utf-8")
        return []


def guardar_json(nombre: str, datos: list) -> bool:
    ruta = ARCHIVOS[nombre]
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(ruta, "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, indent=4, ensure_ascii=False)
    return True


def nuevo_id(prefijo: str) -> str:
    return f"{prefijo}-{uuid.uuid4().hex[:6].upper()}"
