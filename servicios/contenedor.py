from domain.entidades.estudiante import Estudiante
from domain.entidades.usuario import Usuario
from domain.interfaces.exportador import IExportadorEstudiantes
from domain.interfaces.importador import IImportadorEstudiantes
from domain.interfaces.repositorio import IRepositorioEstudiante
from domain.interfaces.repositorio_docente import IRepositorioDocente
from domain.interfaces.repositorio_materia import IRepositorioMateria
from domain.interfaces.repositorio_usuario import IRepositorioUsuario
from factories.persona_factory import DocenteFactory, EstudianteFactory
from infraestructura.excel.excel_estudiante_reader import ExcelImportadorEstudiantes
from infraestructura.excel.excel_estudiante_writer import ExcelExportadorEstudiantes
from infraestructura.repositorios.json_docente_repo import RepositorioDocenteJson
from infraestructura.repositorios.json_estudiante_repo import RepositorioEstudianteJson
from infraestructura.repositorios.json_materia_repo import RepositorioMateriaJson
from infraestructura.repositorios.json_usuario_repo import RepositorioUsuarioJson
from infraestructura.utilidades.almacenamiento import iniciar_datos
from servicios.autenticacion_servicio import AutenticacionServicio
from servicios.gestor_academico import GestorAcademico
from servicios.matricula_servicio import MatriculaServicio


class ContenedorAplicacion:
    """
    FACADE (patrón estructural — Refactoring.Guru):
    Proporciona una interfaz unificada y simplificada al subsistema de servicios
    (GestorAcademico, AutenticacionServicio, MatriculaServicio).
    Oculta la complejidad de repositorios JSON, fábricas, importadores/exportadores Excel
    y la interacción entre múltiples servicios.

    También actúa como COMPOSITION ROOT: único lugar donde se instancian implementaciones
    concretas (inyección de dependencias hacia los servicios).
    """

    def __init__(
        self,
        gestor: GestorAcademico,
        autenticacion: AutenticacionServicio,
        matricula: MatriculaServicio,
    ) -> None:
        self._gestor = gestor
        self._autenticacion = autenticacion
        self._matricula = matricula

    @property
    def gestor(self) -> GestorAcademico:
        """Subsistema académico: estudiantes, materias, calificaciones y Excel."""
        return self._gestor

    @property
    def autenticacion(self) -> AutenticacionServicio:
        """Subsistema de registro e inicio de sesión."""
        return self._autenticacion

    @property
    def matricula(self) -> MatriculaServicio:
        """Subsistema de aulas, cursos, postulantes y matrículas."""
        return self._matricula

    def iniciar_sesion(self, cedula: str, contrasena: str) -> Usuario:
        """Delegación a AutenticacionServicio — la vista no conoce el subsistema."""
        return self._autenticacion.iniciar_sesion(cedula, contrasena)

    def registrar_usuario(self, datos: dict, contrasena: str, rol: str) -> Usuario:
         """Delegación a AutenticacionServicio: la Vista de registro no necesita
            saber que existe ese servicio, solo llama al Facade."""
        return self._autenticacion.registrar(datos, contrasena, rol)

    def obtener_perfil_estudiante(self, cedula: str) -> Estudiante | None:
         """Igual que arriba: oculta a la Vista que el perfil vive en
            AutenticacionServicio y no en GestorAcademico."""
        return self._autenticacion.obtener_perfil_estudiante(cedula)


def crear_contenedor() -> ContenedorAplicacion:
    """COMPOSITION ROOT: único lugar que instancia implementaciones concretas e inyecta dependencias."""
    iniciar_datos()

    # --- Implementaciones concretas (capa infraestructura) ---
    repo_estudiantes: IRepositorioEstudiante = RepositorioEstudianteJson()
    repo_docentes: IRepositorioDocente = RepositorioDocenteJson()
    repo_materias: IRepositorioMateria = RepositorioMateriaJson()
    repo_usuarios: IRepositorioUsuario = RepositorioUsuarioJson()

    # FACTORY METHOD: fábricas para crear personas según tipo
    fabrica_estudiante = EstudianteFactory()
    fabrica_docente = DocenteFactory()

    # Dependencias de Excel inyectadas al gestor
    importador: IImportadorEstudiantes = ExcelImportadorEstudiantes(fabrica_estudiante)
    exportador: IExportadorEstudiantes = ExcelExportadorEstudiantes()

    # --- Servicios con dependencias inyectadas (principio D de SOLID) ---
    gestor = GestorAcademico(
        repo_estudiantes=repo_estudiantes,
        repo_materias=repo_materias,
        repo_docentes=repo_docentes,
        importador=importador,
        exportador=exportador,
        fabrica_estudiante=fabrica_estudiante,
    )

    autenticacion = AutenticacionServicio(
        repo_usuario=repo_usuarios,
        repo_estudiante=repo_estudiantes,
        repo_docente=repo_docentes,
        fabrica_estudiante=fabrica_estudiante,
        fabrica_docente=fabrica_docente,
    )

    matricula = MatriculaServicio()

    # FACADE: ensambla el subsistema y expone una única interfaz a las vistas
    return ContenedorAplicacion(
        gestor=gestor,
        autenticacion=autenticacion,
        matricula=matricula,
    )
