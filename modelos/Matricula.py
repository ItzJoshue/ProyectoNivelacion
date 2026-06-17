"""
Modelo Matricula

Representa la relación entre estudiante,
curso y aula.
"""


class Matricula:
    def __init__(self, id, estudiante_id, curso_id, aula_id):
        self.id = id
        self.estudiante_id = estudiante_id
        self.curso_id = curso_id
        self.aula_id = aula_id

    def to_dict(self):
        return {
            "id": self.id,
            "estudiante_id": self.estudiante_id,
            "curso_id": self.curso_id,
            "aula_id": self.aula_id
        }

    @classmethod
    def from_dict(cls, datos):
        return cls(
            datos.get("id", ""),
            datos.get("estudiante_id", ""),
            datos.get("curso_id", ""),
            datos.get("aula_id", "")
        )