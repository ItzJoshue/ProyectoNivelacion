class Matricula:
    """Relación entre estudiante, curso y aula."""

    def __init__(
        self,
        id_matricula: str,
        cedula_estudiante: str,
        id_curso: str,
        id_aula: str,
    ) -> None:
        self._id = id_matricula
        self._cedula_estudiante = cedula_estudiante.strip()
        self._id_curso = id_curso
        self._id_aula = id_aula

    @property
    def id(self) -> str:
        return self._id

    @property
    def cedula_estudiante(self) -> str:
        return self._cedula_estudiante

    @property
    def id_curso(self) -> str:
        return self._id_curso

    @property
    def id_aula(self) -> str:
        return self._id_aula

    def to_dict(self) -> dict:
        return {
            "id": self._id,
            "cedula_estudiante": self._cedula_estudiante,
            "id_curso": self._id_curso,
            "id_aula": self._id_aula,
        }

    @classmethod
    def from_dict(cls, datos: dict) -> "Matricula":
        # Compatibilidad con JSON de la rama Modulosss (estudiante_id)
        cedula = datos.get("cedula_estudiante") or datos.get("estudiante_id", "")
        return cls(
            id_matricula=str(datos.get("id", "")),
            cedula_estudiante=str(cedula),
            id_curso=str(datos.get("curso_id", datos.get("id_curso", ""))),
            id_aula=str(datos.get("aula_id", datos.get("id_aula", ""))),
        )
