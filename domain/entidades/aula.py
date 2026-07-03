class Aula:
    """Aula física disponible para cursos de nivelación (encapsulamiento)."""

    def __init__(self, id_aula: str, codigo: str, capacidad: int) -> None:
        self._id = id_aula
        self._codigo = codigo.strip().upper()
        self._capacidad = capacidad

    @property
    def id(self) -> str:
        return self._id

    @property
    def codigo(self) -> str:
        return self._codigo

    @property
    def capacidad(self) -> int:
        return self._capacidad

    @capacidad.setter
    def capacidad(self, valor: int) -> None:
        if valor <= 0:
            raise ValueError("La capacidad debe ser mayor a cero.")
        self._capacidad = valor

    def to_dict(self) -> dict:
        return {"id": self._id, "codigo": self._codigo, "capacidad": self._capacidad}

    @classmethod
    def from_dict(cls, datos: dict) -> "Aula":
        return cls(
            id_aula=str(datos.get("id", "")),
            codigo=str(datos.get("codigo", "")),
            capacidad=int(datos.get("capacidad", 0)),
        )
