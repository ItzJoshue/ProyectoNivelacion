"""
Modelo Estudiante

Representa un estudiante registrado en el sistema.
Se utiliza para almacenar información académica básica.
"""


class Estudiante:
    def __init__(self, id, nombre, cedula, carrera, correo):
        self.id = id
        self.nombre = nombre
        self.cedula = cedula
        self.carrera = carrera
        self.correo = correo

    def to_dict(self):
        """
        Convierte el objeto a diccionario para guardar en JSON.
        """
        return {
            "id": self.id,
            "nombre": self.nombre,
            "cedula": self.cedula,
            "carrera": self.carrera,
            "correo": self.correo
        }

    @classmethod
    def from_dict(cls, datos):
        """
        Crea un objeto Estudiante desde un diccionario.
        """
        return cls(
            datos.get("id", ""),
            datos.get("nombre", ""),
            datos.get("cedula", ""),
            datos.get("carrera", ""),
            datos.get("correo", "")
        )