class Materia:
    """Materia de nivelación con código y créditos."""

    def __init__(self, codigo: str, nombre: str, creditos: int = 3) -> None:
        self._codigo = codigo.strip().upper()
        self._nombre = nombre.strip()
        self._creditos = creditos

    @property
    def codigo(self) -> str:
        return self._codigo

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        if not valor or not valor.strip():
            raise ValueError("El nombre de la materia no puede estar vacío.")
        self._nombre = valor.strip()

    @property
    def creditos(self) -> int:
        return self._creditos

    @creditos.setter
    def creditos(self, valor: int) -> None:
        if valor <= 0:
            raise ValueError("Los créditos deben ser mayores a cero.")
        self._creditos = valor

    def __eq__(self, otro: object) -> bool:
        if not isinstance(otro, Materia):
            return NotImplemented
        return self._codigo == otro._codigo

    def __hash__(self) -> int:
        return hash(self._codigo)

    def __repr__(self) -> str:
        return f"Materia(codigo={self._codigo!r}, nombre={self._nombre!r})"
