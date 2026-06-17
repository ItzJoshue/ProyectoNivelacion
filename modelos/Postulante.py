"""
Modelo Postulante

Representa una persona que aspira a ingresar
a la institución.
"""


class Postulante:
    def __init__(self, id, nombre, cedula, carrera, puntaje):
        self.id = id
        self.nombre = nombre
        self.cedula = cedula
        self.carrera = carrera
        self.puntaje = puntaje

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "cedula": self.cedula,
            "carrera": self.carrera,
            "puntaje": self.puntaje
        }

    @classmethod
    def from_dict(cls, datos):
        return cls(
            datos.get("id", ""),
            datos.get("nombre", ""),
            datos.get("cedula", ""),
            datos.get("carrera", ""),
            datos.get("puntaje", "")
        )