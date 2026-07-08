"""
ABSTRACCIÓN Y DIAGRAMAS DE MODELADO:
Capa de dominio que representa el modelo conceptual del sistema académico ULEAM.
Las entidades abstraen la realidad del negocio (estudiantes, docentes, materias…)
sin depender de JSON, Excel ni interfaz gráfica.

Diagrama de clases (relaciones principales):
    Persona (abstracta)
      ├── Estudiante  — tiene materias[] y calificaciones{}
      └── Docente     — tiene materias_asignadas[]
    Materia           — entidad independiente referenciada por nombre
    Usuario           — asociado a Persona por cédula (autenticación)

CLASES, OBJETOS Y RELACIONES:
Cada archivo define una clase; al instanciarla se crea un objeto con estado propio.
Ejemplo: Estudiante(cedula="123", ...) es un objeto que se relaciona con Materia
mediante la lista _materias y con Usuario mediante la cédula compartida.
"""

from domain.entidades.estudiante import Estudiante
from domain.entidades.docente import Docente
from domain.entidades.materia import Materia
from domain.entidades.persona import Persona

__all__ = ["Persona", "Estudiante", "Docente", "Materia"]
