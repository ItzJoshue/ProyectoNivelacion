from dataclasses import dataclass

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


@dataclass
class ContenedorAplicacion:
    """
    COMPOSITION ROOT — único lugar donde se instancian implementaciones concretas.
    Aquí ocurre la INYECCIÓN DE DEPENDENCIAS hacia los servicios.
    """

    gestor: GestorAcademico
    autenticacion: AutenticacionServicio
    matricula: MatriculaServicio


def crear_contenedor() -> ContenedorAplicacion:
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

    return ContenedorAplicacion(
        gestor=gestor,
        autenticacion=autenticacion,
        matricula=matricula,
    )
