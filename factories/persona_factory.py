from abc import ABC, abstractmethod

from domain.entidades.docente import Docente
from domain.entidades.estudiante import Estudiante
from domain.entidades.persona import Persona


class PersonaFactory(ABC):
    """
    FACTORY METHOD (patrón creacional — Refactoring.Guru):
    Cada subclase define cómo crear un tipo concreto de Persona.
    """

    @abstractmethod
    def crear(self, datos: dict) -> Persona:
        pass


class EstudianteFactory(PersonaFactory):
    def crear(self, datos: dict) -> Estudiante:
        # Factory Method concreto para Estudiante
        return Estudiante(
            cedula=str(datos.get("cedula", "")).strip(),
            nombre=str(datos.get("nombre", "")).strip(),
            apellido=str(datos.get("apellido", "")).strip(),
            carrera=str(datos.get("carrera", "")).strip(),
            email=str(datos.get("email", "")).strip(),
        )


class DocenteFactory(PersonaFactory):
    def crear(self, datos: dict) -> Docente:
        return Docente(
            cedula=str(datos.get("cedula", "")).strip(),
            nombre=str(datos.get("nombre", "")).strip(),
            apellido=str(datos.get("apellido", "")).strip(),
            departamento=str(datos.get("departamento", "")).strip(),
        )


class PersonaFactoryCreator:
    """Selector de fábricas — Open/Closed: agregar tipos sin modificar clientes."""

    _fabricas: dict[str, PersonaFactory] = {
        "estudiante": EstudianteFactory(),
        "docente": DocenteFactory(),
    }

    @classmethod
    def obtener_fabrica(cls, tipo: str) -> PersonaFactory:
        fabrica = cls._fabricas.get(tipo.lower())
        if fabrica is None:
            raise ValueError(f"Tipo de persona no soportado: {tipo}")
        return fabrica
