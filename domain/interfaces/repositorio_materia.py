from abc import ABC, abstractmethod

from domain.entidades.materia import Materia


class IRepositorioMateria(ABC):
    """Contrato para persistencia de materias."""

    @abstractmethod
    def guardar(self, materia: Materia) -> None:
        pass

    @abstractmethod
    def obtener_todas(self) -> list[Materia]:
        pass

    @abstractmethod
    def buscar_por_codigo(self, codigo: str) -> Materia | None:
        pass

    @abstractmethod
    def eliminar(self, codigo: str) -> bool:
        pass
