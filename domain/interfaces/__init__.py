from domain.interfaces.exportador import IExportadorEstudiantes
from domain.interfaces.importador import IImportadorEstudiantes
from domain.interfaces.repositorio import IRepositorioEstudiante
from domain.interfaces.repositorio_materia import IRepositorioMateria

__all__ = [
    "IRepositorioEstudiante",
    "IRepositorioMateria",
    "IImportadorEstudiantes",
    "IExportadorEstudiantes",
]
