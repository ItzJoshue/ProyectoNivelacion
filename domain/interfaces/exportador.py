from abc import ABC, abstractmethod

from domain.entidades.estudiante import Estudiante


class IExportadorEstudiantes(ABC):
    """Interfaz para exportar estudiantes a formatos externos."""

    @abstractmethod
    def exportar(self, estudiantes: list[Estudiante], ruta: str) -> None:
        pass
