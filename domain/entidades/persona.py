from abc import ABC, abstractmethod


class Persona(ABC):
    """
    HERENCIA: clase base abstracta de la que heredan Estudiante y Docente.

    POLIMORFISMO CON CLASES ABSTRACTAS: define el contrato común (obtener_rol,
    obtener_resumen) que cada subclase implementa de forma distinta.

    TEMPLATE METHOD (patrón de comportamiento): la clase base fija la estructura
    común (cedula, nombre, apellido, nombre_completo) y delega los pasos variables
    a las subclases mediante métodos abstractos.
    """

    def __init__(self, cedula: str, nombre: str, apellido: str) -> None:
        # CONSTRUCTOR + ENCAPSULAMIENTO: atributos privados accedidos vía @property
        self._cedula = cedula
        self._nombre = nombre
        self._apellido = apellido

    @property
    def cedula(self) -> str:
        return self._cedula

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        if not valor or not valor.strip():
            raise ValueError("El nombre no puede estar vacío.")
        self._nombre = valor.strip()

    @property
    def apellido(self) -> str:
        return self._apellido

    @apellido.setter
    def apellido(self, valor: str) -> None:
        if not valor or not valor.strip():
            raise ValueError("El apellido no puede estar vacío.")
        self._apellido = valor.strip()

    @property
    def nombre_completo(self) -> str:
        return f"{self._nombre} {self._apellido}"

    @abstractmethod
    def obtener_rol(self) -> str:
        """POLIMORFISMO (ABC): cada subclase retorna su rol académico."""

    @abstractmethod
    def obtener_resumen(self) -> str:
        """POLIMORFISMO (ABC): cada subclase genera su propio resumen."""

    def __eq__(self, otro: object) -> bool:
        if not isinstance(otro, Persona):
            return NotImplemented
        return self._cedula == otro._cedula

    def __hash__(self) -> int:
        return hash(self._cedula)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(cedula={self._cedula!r})"
