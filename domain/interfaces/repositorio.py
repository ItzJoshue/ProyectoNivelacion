from abc import ABC, abstractmethod

from domain.entidades.estudiante import Estudiante


class IRepositorioEstudiante(ABC):
    """
    INTERFAZ (ABC): contrato abstracto para persistencia de estudiantes.
    POLIMORFISMO CON INTERFACES: GestorAcademico depende de esta abstracción;
    RepositorioEstudianteJson o RepositorioEstudianteMemoria pueden sustituirse.
    """

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
