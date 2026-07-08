from domain.entidades.persona import Persona

class Postulante(Persona):
    """Persona que aspira a ingresar al proceso de nivelación (Unidad 2: Herencia)."""

    def __init__(
        self,
        id_postulante: str,
        nombre: str,
        cedula: str,
        carrera: str,
        puntaje: float,
        correo: str = "",
    ) -> None:
        # Reutilizamos el constructor de la clase abstracta Persona para id, nombre y correo (herencia)
        super().__init__(id_persona=id_postulante, nombre=nombre, email=correo)
        self._cedula = cedula.strip()
        self._carrera = carrera.strip()
        self._puntaje = puntaje

    @property
    def cedula(self) -> str:
        return self._cedula

    @property
    def carrera(self) -> str:
        return self._carrera

    @property
    def puntaje(self) -> float:
        return self._puntaje

    def obtener_rol(self) -> str:
        """Implementación obligatoria del método abstracto de Persona (Polimorfismo)."""
        return "POSTULANTE"

    def to_dict(self) -> dict:
        """Serializa los datos combinando los campos heredados y los propios."""
        # Obtenemos el diccionario base de Persona (id, nombre, email, rol)
        datos = super().to_dict()
        # Agregamos los atributos específicos de Postulante
        datos.update({
            "cedula": self._cedula,
            "carrera": self._carrera,
            "puntaje": self._puntaje
        })
        return datos

    @classmethod
    def from_dict(cls, datos: dict) -> "Postulante":
        return cls(
            id_postulante=str(datos.get("id", "")),
            nombre=str(datos.get("nombre", "")),
            cedula=str(datos.get("cedula", "")),
            carrera=str(datos.get("carrera", "")),
            puntaje=float(datos.get("puntaje", 0.0)),
            correo=str(datos.get("email", datos.get("correo", ""))),
        )
