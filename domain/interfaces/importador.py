from abc import ABC, abstractmethod

from domain.entidades.estudiante import Estudiante


class IImportadorEstudiantes(ABC):
    """Interfaz para importar estudiantes desde fuentes externas."""

    @abstractmethod
    def importar(self, ruta: str) -> list[Estudiante]:
        pass
