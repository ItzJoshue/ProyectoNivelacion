from .json_service import JsonService

from .estudiante_service import EstudianteService
from .profesor_service import ProfesorService
from .aula_service import AulaService
from .curso_service import CursoService
from .postulante_service import PostulanteService
from .matricula_service import MatriculaService

__all__ = [
    "JsonService",
    "EstudianteService",
    "ProfesorService",
    "AulaService",
    "CursoService",
    "PostulanteService",
    "MatriculaService",
]