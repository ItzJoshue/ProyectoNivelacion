import hashlib


class Usuario:
    """
    CLASE de autenticación. RELACIÓN: se vincula a Persona por cédula.
    ENCAPSULAMIENTO: la contraseña se guarda hasheada y nunca se expone.
    """

    ROLES_VALIDOS = ("estudiante", "docente")

    def __init__(self, cedula: str, contrasena: str, rol: str, registrar_hash: bool = True) -> None:
        # CONSTRUCTOR con parámetro opcional registrar_hash (sobrecarga de comportamiento)
        self._cedula = cedula.strip()
        self._rol = rol.strip().lower()
        if self._rol not in self.ROLES_VALIDOS:
            raise ValueError(f"Rol inválido. Use: {', '.join(self.ROLES_VALIDOS)}")
        # Encapsulamiento: la contraseña nunca se expone en texto plano
        self._contrasena_hash = (
            self._hash(contrasena) if registrar_hash else contrasena
        )

    @staticmethod
    def _hash(contrasena: str) -> str:
        return hashlib.sha256(contrasena.encode("utf-8")).hexdigest()

    @property
    def cedula(self) -> str:
        return self._cedula

    @property
    def rol(self) -> str:
        return self._rol

    def verificar_contrasena(self, contrasena: str) -> bool:
        return self._contrasena_hash == self._hash(contrasena)

    def to_dict(self) -> dict[str, str]:
        return {
            "cedula": self._cedula,
            "contrasena_hash": self._contrasena_hash,
            "rol": self._rol,
        }

    @classmethod
    def from_dict(cls, datos: dict) -> "Usuario":
        return cls(
            cedula=str(datos.get("cedula", "")),
            contrasena=str(datos.get("contrasena_hash", "")),
            rol=str(datos.get("rol", "")),
            registrar_hash=False,
        )
