from functools import singledispatchmethod
from domain.entidades.persona import Persona

NOTA_MINIMA_APROBACION = 7.0


class EvaluadorAcademico:
    """Clase de servicio/estrategia que maneja las reglas de negocio académicas (SOLID: SRP)."""

    @staticmethod
    def calcular_promedio(calificaciones: dict[str, float]) -> float:
        if not calificaciones:
            return 0.0
        return round(sum(calificaciones.values()) / len(calificaciones), 2)

    @staticmethod
    def determinar_estado(promedio: float) -> str:
        if promedio == 0.0:
            return "Sin calificar"
        return "Aprobado" if promedio >= NOTA_MINIMA_APROBACION else "Reprobado"


class Estudiante(Persona):
    """
    HERENCIA: extiende Persona y agrega atributos propios del dominio académico.

    RELACIÓN ENTRE CLASES: un Estudiante se asocia con Materia (lista _materias)
    y mantiene calificaciones por materia (dict _calificaciones).
    """

    def __init__(
        self,
        cedula: str,
        nombre: str,
        apellido: str,
        carrera: str = "",
        email: str = "",
    ) -> None:
        super().__init__(cedula, nombre, apellido)
        self._carrera = carrera
        self._email = email
        self._materias: list[str] = []
        self._calificaciones: dict[str, float] = {}

    @property
    def carrera(self) -> str:
        return self._carrera

    @carrera.setter
    def carrera(self, valor: str) -> None:
        self._carrera = valor.strip()

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, valor: str) -> None:
        self._email = valor.strip()

    @property
    def materias(self) -> tuple[str, ...]:
        return tuple(self._materias)

    @property
    def calificaciones(self) -> dict[str, float]:
        return dict(self._calificaciones)

    @property
    def promedio(self) -> float:
        # Se delega la lógica al evaluador especializado
        return EvaluadorAcademico.calcular_promedio(self._calificaciones)

    @property
    def estado_academico(self) -> str:
        # Se delega la lógica al evaluador especializado
        return EvaluadorAcademico.determinar_estado(self.promedio)

    def obtener_rol(self) -> str:
        """POLIMORFISMO (ABC): implementación concreta del método abstracto."""
        return "Estudiante"

    def obtener_resumen(self) -> str:
        """POLIMORFISMO (ABC): resumen específico del estudiante."""
        return (
            f"{self.nombre_completo} ({self._cedula}) - {self._carrera or 'Sin carrera'} "
            f"| Promedio: {self.promedio} | {self.estado_academico}"
        )

    def asignar_materia(self, materia: str) -> None:
        """MÉTODO de negocio: agrega una materia a la lista del estudiante."""
        materia = materia.strip()
        if materia and materia not in self._materias:
            self._materias.append(materia)

    def registrar_calificacion(self, materia: str, nota: float) -> None:
        if not 0 <= nota <= 10:
            raise ValueError("La calificación debe estar entre 0 y 10.")
        self._calificaciones[materia.strip()] = round(nota, 2)

    def registrar_calificaciones(self, calificaciones: dict[str, float]) -> None:
        for materia, nota in calificaciones.items():
            self.registrar_calificacion(materia, nota)

    @singledispatchmethod
    def consultar_calificacion(self, consulta) -> float | dict[str, float]:
        """SOBRECARGA DE MÉTODOS: un mismo nombre, distinto comportamiento según el tipo."""
        raise TypeError("Consulta no soportada. Use str o list[str].")

    @consultar_calificacion.register
    def _(self, materia: str) -> float:
        return self._calificaciones.get(materia.strip(), 0.0)

    @consultar_calificacion.register
    def _(self, materias: list) -> dict[str, float]:
        return {m: self._calificaciones.get(m.strip(), 0.0) for m in materias}

    def to_dict(self) -> dict[str, str | float | list | dict]:
        return {
            "cedula": self._cedula,
            "nombre": self._nombre,
            "apellido": self._apellido,
            "carrera": self._carrera,
            "email": self._email,
            "promedio": self.promedio,
            "materias": list(self._materias),
            "calificaciones": dict(self._calificaciones),
        }

    @classmethod
    def from_dict(cls, datos: dict) -> "Estudiante":
        estudiante = cls(
            cedula=str(datos.get("cedula", "")),
            nombre=str(datos.get("nombre", "")),
            apellido=str(datos.get("apellido", "")),
            carrera=str(datos.get("carrera", "")),
            email=str(datos.get("email", datos.get("correo", ""))),
        )
        for materia in datos.get("materias", []):
            estudiante.asignar_materia(str(materia))
        for materia, nota in datos.get("calificaciones", {}).items():
            try:
                estudiante.registrar_calificacion(str(materia), float(nota))
            except ValueError:
                continue
        return estudiante
