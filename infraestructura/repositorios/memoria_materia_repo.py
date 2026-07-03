from domain.entidades.materia import Materia
from domain.interfaces.repositorio_materia import IRepositorioMateria


class RepositorioMateriaMemoria(IRepositorioMateria):
    """Implementación en memoria del repositorio de materias."""

    def __init__(self) -> None:
        self._materias: dict[str, Materia] = {}

    def guardar(self, materia: Materia) -> None:
        self._materias[materia.codigo] = materia

    def obtener_todas(self) -> list[Materia]:
        return list(self._materias.values())

    def buscar_por_codigo(self, codigo: str) -> Materia | None:
        return self._materias.get(codigo.strip().upper())

    def eliminar(self, codigo: str) -> bool:
        return self._materias.pop(codigo.strip().upper(), None) is not None
