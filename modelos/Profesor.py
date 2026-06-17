"""
Modelo Profesor

Representa un docente del sistema académico.
"""


class Profesor:
    def __init__(self, id, nombre, cedula, materia, correo):
        self.id = id
        self.nombre = nombre
        self.cedula = cedula
        self.materia = materia
        self.correo = correo

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "cedula": self.cedula,
            "materia": self.materia,
            "correo": self.correo
        }

    @classmethod
    def from_dict(cls, datos):
        return cls(
            datos.get("id", ""),
            datos.get("nombre", ""),
            datos.get("cedula", ""),
            datos.get("materia", ""),
            datos.get("correo", "")
        )