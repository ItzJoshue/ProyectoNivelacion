from domain.entidades.persona import Persona


class Docente(Persona):
    """HERENCIA: subclase de Persona especializada en docentes de nivelación."""

    def __init__(
        self,
        cedula: str,
        nombre: str,
        apellido: str,
        departamento: str = "",
    ) -> None:
        super().__init__(cedula, nombre, apellido)
        self._departamento = departamento
        self._materias_asignadas: list[str] = []

    @property
    def departamento(self) -> str:
        return self._departamento

    @departamento.setter
    def departamento(self, valor: str) -> None:
        self._departamento = valor.strip()

    @property
    def materias_asignadas(self) -> tuple[str, ...]:
        return tuple(self._materias_asignadas)

    def obtener_rol(self) -> str:
        """POLIMORFISMO (ABC): implementación concreta del método abstracto."""
        return "Docente"

    def obtener_resumen(self) -> str:
        """POLIMORFISMO (ABC): resumen específico del docente."""
        materias = ", ".join(self._materias_asignadas) or "Sin materias"
        return f"{self.nombre_completo} ({self._cedula}) - {self._departamento} | {materias}"

    def asignar_materia(self, materia: str) -> None:
        materia = materia.strip()
        if materia and materia not in self._materias_asignadas:
            self._materias_asignadas.append(materia)

    def to_dict(self) -> dict[str, str | list]:
        return {
            "cedula": self._cedula,
            "nombre": self._nombre,
            "apellido": self._apellido,
            "departamento": self._departamento,
            "materias_asignadas": list(self._materias_asignadas),
        }

    @classmethod
    def from_dict(cls, datos: dict) -> "Docente":
        docente = cls(
            cedula=str(datos.get("cedula", "")),
            nombre=str(datos.get("nombre", "")),
            apellido=str(datos.get("apellido", "")),
            departamento=str(datos.get("departamento", datos.get("materia", ""))),
        )
        for materia in datos.get("materias_asignadas", []):
            docente.asignar_materia(str(materia))
        return docente
