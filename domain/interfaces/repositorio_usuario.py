from abc import ABC, abstractmethod

from domain.entidades.usuario import Usuario


class IRepositorioUsuario(ABC):
    """
    Interface Segregation (SOLID): contrato mínimo para usuarios.
    Dependency Inversion: los servicios dependen de esta abstracción.
    """

    @abstractmethod
    def guardar(self, usuario: Usuario) -> None:
        pass

    @abstractmethod
    def buscar_por_cedula(self, cedula: str) -> Usuario | None:
        pass

    @abstractmethod
    def obtener_todos(self) -> list[Usuario]:
        pass
