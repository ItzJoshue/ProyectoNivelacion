from abc import ABC, abstractmethod


class Persona(ABC):
    """
    HERENCIA + POLIMORFISMO (clase abstracta):
    Estudiante y Docente heredan de Persona y redefinen métodos abstractos.
    Referencia: https://ellibrodepython.com/ (POO) | https://refactoring.guru/ (SOLID)
    """

    def __init__(self, cedula: str, nombre: str, apellido: str) -> None:
        # ENCAPSULAMIENTO: atributos privados accedidos vía @property
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
        """Retorna el rol académico de la persona."""

    @abstractmethod
    def obtener_resumen(self) -> str:
        """Retorna un resumen legible de la persona."""

    def __eq__(self, otro: object) -> bool:
        if not isinstance(otro, Persona):
            return NotImplemented
        return self._cedula == otro._cedula

    def __hash__(self) -> int:
        return hash(self._cedula)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(cedula={self._cedula!r})"
