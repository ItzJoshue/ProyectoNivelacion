from domain.entidades.estudiante import Estudiante
from domain.interfaces.repositorio import IRepositorioEstudiante


class RepositorioEstudianteMemoria(IRepositorioEstudiante):
    """POLIMORFISMO CON INTERFACES: implementación concreta del contrato
    IRepositorioEstudiante, pero guardando todo en memoria (útil para pruebas)
    en vez de JSON. El servicio que la usa no nota la diferencia."""

    def __init__(self) -> None:
        self._estudiantes: dict[str, Estudiante] = {}

    def guardar(self, estudiante: Estudiante) -> None:
        if not estudiante.cedula:
            raise ValueError("La cédula del estudiante es obligatoria.")
        self._estudiantes[estudiante.cedula] = estudiante

    def obtener_todos(self) -> list[Estudiante]:
        return list(self._estudiantes.values())

    def buscar_por_cedula(self, cedula: str) -> Estudiante | None:
        return self._estudiantes.get(cedula.strip())

    def eliminar(self, cedula: str) -> bool:
        return self._estudiantes.pop(cedula.strip(), None) is not None

    def actualizar(self, estudiante: Estudiante) -> None:
        if estudiante.cedula not in self._estudiantes:
            raise KeyError(f"No existe estudiante con cédula {estudiante.cedula}.")
        self._estudiantes[estudiante.cedula] = estudiante
