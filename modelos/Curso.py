"""
Modelo Curso

Representa una asignatura o curso ofertado.
"""


class Curso:
    def __init__(self, id, nombre, cupos):
        self.id = id
        self.nombre = nombre
        self.cupos = cupos

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "cupos": self.cupos
        }

    @classmethod
    def from_dict(cls, datos):
        return cls(
            datos.get("id", ""),
            datos.get("nombre", ""),
            datos.get("cupos", "")
        )