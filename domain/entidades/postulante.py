class Postulante:
    """Persona que aspira a ingresar al proceso de nivelación."""

    def __init__(
        self,
        id_postulante: str,
        nombre: str,
        cedula: str,
        carrera: str,
        puntaje: float,
        correo: str = "",
    ) -> None:
        self._id = id_postulante
        self._nombre = nombre.strip()
        self._cedula = cedula.strip()
        self._carrera = carrera.strip()
        self._puntaje = puntaje
        self._correo = correo.strip()

    @property
    def id(self) -> str:
        return self._id

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def cedula(self) -> str:
        return self._cedula

    @property
    def carrera(self) -> str:
        return self._carrera

    @property
    def puntaje(self) -> float:
        return self._puntaje

    @property
    def correo(self) -> str:
        return self._correo

    def to_dict(self) -> dict:
        return {
            "id": self._id,
            "nombre": self._nombre,
            "cedula": self._cedula,
            "carrera": self._carrera,
            "puntaje": self._puntaje,
            "correo": self._correo,
        }

    @classmethod
    def from_dict(cls, datos: dict) -> "Postulante":
        return cls(
            id_postulante=str(datos.get("id", "")),
            nombre=str(datos.get("nombre", "")),
            cedula=str(datos.get("cedula", "")),
            carrera=str(datos.get("carrera", "")),
            puntaje=float(datos.get("puntaje", 0)),
            correo=str(datos.get("correo", "")),
        )
