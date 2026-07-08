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
        # Validación Defensiva (Control de Estado - Unidad 1) antes de la instanciación
        cedula = str(datos.get("cedula", "")).strip()
        nombre = str(datos.get("nombre", "")).strip()
        carrera = str(datos.get("carrera", "")).strip()

        if not cedula or not nombre:
            raise ValueError("La cédula y el nombre son campos obligatorios para crear un estudiante.")
        if not carrera:
            raise ValueError("La carrera es un campo estrictamente obligatorio para el estudiante.")

        # Factory Method concreto para Estudiante
        return Estudiante(
            cedula=cedula,
            nombre=nombre,
            apellido=str(datos.get("apellido", "")).strip(),
            carrera=carrera,
            email=str(datos.get("email", "")).strip(),
        )




class DocenteFactory(PersonaFactory):
    def crear(self, datos: dict) -> Docente:
        # Validación Defensiva (Control de Estado - Unidad 1) antes de la instanciación
        cedula = str(datos.get("cedula", "")).strip()
        nombre = str(datos.get("nombre", "")).strip()
        departamento = str(datos.get("departamento", "")).strip()

        if not cedula or not nombre:
            raise ValueError("La cédula y el nombre son campos obligatorios para crear un docente.")
        if not departamento:
            raise ValueError("El departamento es un campo obligatorio para el docente.")

        # Factory Method concreto para Docente
        return Docente(
            cedula=cedula,
            nombre=nombre,
            apellido=str(datos.get("apellido", "")).strip(),
            departamento=departamento,
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
