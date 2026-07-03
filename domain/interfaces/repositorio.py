from abc import ABC, abstractmethod

from domain.entidades.estudiante import Estudiante


class IRepositorioEstudiante(ABC):
    """Contrato para persistencia de estudiantes (Dependency Inversion)."""

    @abstractmethod
    def guardar(self, estudiante: Estudiante) -> None:
        pass

    @abstractmethod
    def obtener_todos(self) -> list[Estudiante]:
        pass

    @abstractmethod
    def buscar_por_cedula(self, cedula: str) -> Estudiante | None:
        pass

    @abstractmethod
    def eliminar(self, cedula: str) -> bool:
        pass

    @abstractmethod
    def actualizar(self, estudiante: Estudiante) -> None:
        pass
