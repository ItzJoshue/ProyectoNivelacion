from domain.entidades.docente import Docente
from domain.entidades.estudiante import Estudiante
from domain.entidades.usuario import Usuario
from domain.interfaces.repositorio import IRepositorioEstudiante
from domain.interfaces.repositorio_docente import IRepositorioDocente
from domain.interfaces.repositorio_usuario import IRepositorioUsuario
from factories.persona_factory import DocenteFactory, EstudianteFactory, PersonaFactoryCreator


class AutenticacionServicio:
    """
    Servicio de registro e inicio de sesión.

    INYECCIÓN DE DEPENDENCIAS: recibe repositorios e interfaces por constructor,
    no crea sus propias dependencias (principio D de SOLID).
    """

    def __init__(
        self,
        repo_usuario: IRepositorioUsuario,
        repo_estudiante: IRepositorioEstudiante,
        repo_docente: IRepositorioDocente,
        fabrica_estudiante: EstudianteFactory | None = None,
        fabrica_docente: DocenteFactory | None = None,
    ) -> None:
        # Dependencias inyectadas — el servicio no conoce JSON ni memoria
        self._repo_usuario = repo_usuario
        self._repo_estudiante = repo_estudiante
        self._repo_docente = repo_docente
        # FACTORY METHOD: fábricas concretas seleccionadas según el rol
        self._fabrica_estudiante = fabrica_estudiante or PersonaFactoryCreator.obtener_fabrica(
            "estudiante"
        )
        self._fabrica_docente = fabrica_docente or PersonaFactoryCreator.obtener_fabrica("docente")

    def registrar(self, datos: dict, contrasena: str, rol: str) -> Usuario:
        cedula = str(datos.get("cedula", "")).strip()
        if not cedula or not contrasena:
            raise ValueError("Cédula y contraseña son obligatorias.")
        if len(contrasena) < 4:
            raise ValueError("La contraseña debe tener al menos 4 caracteres.")
        if self._repo_usuario.buscar_por_cedula(cedula):
            raise ValueError(f"Ya existe una cuenta con cédula {cedula}.")

        rol = rol.lower()
        # POLIMORFISMO + FACTORY METHOD: la fábrica crea el tipo correcto de Persona
        if rol == "estudiante":
            persona = self._fabrica_estudiante.crear(datos)
            self._repo_estudiante.guardar(persona)
        elif rol == "docente":
            persona = self._fabrica_docente.crear(datos)
            self._repo_docente.guardar(persona)
        else:
            raise ValueError("Rol inválido. Use 'estudiante' o 'docente'.")

        usuario = Usuario(cedula, contrasena, rol)
        self._repo_usuario.guardar(usuario)
        return usuario

    def iniciar_sesion(self, cedula: str, contrasena: str) -> Usuario:
        usuario = self._repo_usuario.buscar_por_cedula(cedula.strip())
        if usuario is None or not usuario.verificar_contrasena(contrasena):
            raise ValueError("Cédula o contraseña incorrectas.")
        return usuario

    def obtener_perfil_estudiante(self, cedula: str) -> Estudiante | None:
        return self._repo_estudiante.buscar_por_cedula(cedula)

    def obtener_perfil_docente(self, cedula: str) -> Docente | None:
        return self._repo_docente.buscar_por_cedula(cedula)
