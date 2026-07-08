import json
import os
import uuid
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
_DATA_DIR_PROYECTO = BASE_DIR / "Datos"
_DATA_DIR_LOCAL = Path(os.environ.get("LOCALAPPDATA", Path.home())) / "ProyectoNivelacion" / "Datos"

NOMBRES_ARCHIVOS = (
    "estudiantes",
    "docentes",
    "profesores",
    "usuarios",
    "materias",
    "aulas",
    "cursos",
    "postulantes",
    "matriculas",
)


def _directorio_datos() -> Path:
    """Usa Datos/ del proyecto; si OneDrive no permite escribir, usa AppData local."""
    try:
        _DATA_DIR_PROYECTO.mkdir(parents=True, exist_ok=True)
        probe = _DATA_DIR_PROYECTO / ".write_test"
        probe.write_text("", encoding="utf-8")
        probe.unlink(missing_ok=True)
        return _DATA_DIR_PROYECTO
    except OSError:
        _DATA_DIR_LOCAL.mkdir(parents=True, exist_ok=True)
        return _DATA_DIR_LOCAL


DATA_DIR = _directorio_datos()


def _ruta(nombre: str) -> Path:
    return DATA_DIR / f"{nombre}.json"


def iniciar_datos() -> None:
    """Inicializa archivos JSON vacíos (persistencia de la rama Modulosss)."""
    global DATA_DIR
    DATA_DIR = _directorio_datos()
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    for nombre in NOMBRES_ARCHIVOS:
        ruta = _ruta(nombre)
        if not ruta.exists():
            ruta.write_text("[]", encoding="utf-8")


def leer_json(nombre: str) -> list:
    iniciar_datos()
    ruta = _ruta(nombre)
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
    iniciar_datos()
    ruta = _ruta(nombre)
    with open(ruta, "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, indent=4, ensure_ascii=False)
    return True


def nuevo_id(prefijo: str) -> str:
    return f"{prefijo}-{uuid.uuid4().hex[:6].upper()}"
