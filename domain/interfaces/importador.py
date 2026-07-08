from abc import ABC, abstractmethod

from domain.entidades.estudiante import Estudiante


class IImportadorEstudiantes(ABC):
    """
    INTERFAZ (ABC): contrato para importar estudiantes desde fuentes externas.
    POLIMORFISMO CON INTERFACES: ExcelImportadorEstudiantes implementa este contrato.
    """

    @abstractmethod
    def importar(self, ruta: str) -> list[Estudiante]:
        pass
