from abc import ABC, abstractmethod

from domain.entidades.docente import Docente


class IRepositorioDocente(ABC):
    @abstractmethod
    def guardar(self, docente: Docente) -> None:
        pass

    @abstractmethod
    def obtener_todos(self) -> list[Docente]:
        pass

    @abstractmethod
    def buscar_por_cedula(self, cedula: str) -> Docente | None:
        pass

    @abstractmethod
    def actualizar(self, docente: Docente) -> None:
        pass

    @abstractmethod
    def eliminar(self, cedula: str) -> bool:
        pass
