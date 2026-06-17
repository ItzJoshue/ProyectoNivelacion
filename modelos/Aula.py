"""
Modelo Aula

Representa un aula física disponible para los cursos.
"""


class Aula:
    def __init__(self, id, codigo, capacidad):
        self.id = id
        self.codigo = codigo
        self.capacidad = capacidad

    def to_dict(self):
        return {
            "id": self.id,
            "codigo": self.codigo,
            "capacidad": self.capacidad
        }

    @classmethod
    def from_dict(cls, datos):
        return cls(
            datos.get("id", ""),
            datos.get("codigo", ""),
            datos.get("capacidad", "")
        )