from abc import ABC, abstractmethod

from domain.entidades.estudiante import Estudiante


class IExportadorEstudiantes(ABC):
    """POLIMORFISMO CON INTERFACES: contrato para exportar estudiantes a formatos
    externos. ExcelExportadorEstudiantes implementa este contrato; se podrían
    añadir otros formatos (CSV, PDF) sin tocar el código que ya lo usa."""

    @abstractmethod
    def exportar(self, estudiantes: list[Estudiante], ruta: str) -> None:
        pass
