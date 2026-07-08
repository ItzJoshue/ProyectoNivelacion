class Curso:
    """Curso o asignatura ofertada en el proceso de nivelación."""

    def __init__(self, id_curso: str, nombre: str, carrera: str = "", cupos: int = 30) -> None:
        self._id = id_curso
        self._nombre = nombre.strip()
        self._carrera = carrera.strip()
        self._cupos = cupos

    @property
    def id(self) -> str:
        return self._id

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def carrera(self) -> str:
        return self._carrera

    @property
    def cupos(self) -> int:
        return self._cupos

    @cupos.setter
    def cupos(self, valor: int) -> None:
        if valor <= 0:
            raise ValueError("Los cupos deben ser mayores a cero.")
        self._cupos = valor

    def to_dict(self) -> dict:
        return {
            "id": self._id,
            "nombre": self._nombre,
            "carrera": self._carrera,
            "cupos": self._cupos,
        }

    @classmethod
    def from_dict(cls, datos: dict) -> "Curso":
        # Flexibilidad OCP/SRP: mapeo seguro para no romper dependencias con la infraestructura JSON
        id_curso = datos.get("id") or datos.get("id_curso") or datos.get("curso_id", "")
        
        return cls(
            id_curso=str(id_curso),
            nombre=str(datos.get("nombre", "")),
            carrera=str(datos.get("carrera", "")),
            cupos=int(datos.get("cupos", 30)),
        )
