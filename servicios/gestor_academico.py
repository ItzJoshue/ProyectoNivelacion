from domain.entidades.docente import Docente
from domain.entidades.estudiante import Estudiante
from domain.entidades.materia import Materia
from domain.entidades.persona import Persona
from domain.interfaces.exportador import IExportadorEstudiantes
from domain.interfaces.importador import IImportadorEstudiantes
from domain.interfaces.repositorio import IRepositorioEstudiante
from domain.interfaces.repositorio_docente import IRepositorioDocente
from domain.interfaces.repositorio_materia import IRepositorioMateria
from factories.persona_factory import EstudianteFactory, PersonaFactoryCreator


class GestorAcademico:
    """
    Servicio de aplicación con INYECCIÓN DE DEPENDENCIAS.
    Depende de abstracciones (interfaces ABC), no de JSON/memoria (SOLID - D).
    """

    def __init__(
        self,
        repo_estudiantes: IRepositorioEstudiante,
        repo_materias: IRepositorioMateria,
        repo_docentes: IRepositorioDocente | None = None,
        importador: IImportadorEstudiantes | None = None,
        exportador: IExportadorEstudiantes | None = None,
        fabrica_estudiante: EstudianteFactory | None = None,
    ) -> None:
        # INYECCIÓN DE DEPENDENCIAS: las abstracciones se reciben por constructor
        self._repo_estudiantes = repo_estudiantes
        self._repo_materias = repo_materias
        self._repo_docentes = repo_docentes
        self._importador = importador
        self._exportador = exportador
        self._fabrica_estudiante = fabrica_estudiante or PersonaFactoryCreator.obtener_fabrica(
            "estudiante"
        )

    def registrar_estudiante(self, datos: dict) -> Estudiante:
        # FACTORY METHOD: la fábrica encapsula la creación del objeto
        estudiante = self._fabrica_estudiante.crear(datos)
        if self._repo_estudiantes.buscar_por_cedula(estudiante.cedula):
            raise ValueError(f"Ya existe un estudiante con cédula {estudiante.cedula}.")
        self._repo_estudiantes.guardar(estudiante)
        return estudiante

    def actualizar_estudiante(self, datos: dict) -> Estudiante:
        cedula = str(datos.get("cedula", "")).strip()
        existente = self._repo_estudiantes.buscar_por_cedula(cedula)
        if existente is None:
            raise KeyError(f"No existe estudiante con cédula {cedula}.")

        existente.nombre = str(datos.get("nombre", existente.nombre))
        existente.apellido = str(datos.get("apellido", existente.apellido))
        existente.carrera = str(datos.get("carrera", existente.carrera))
        existente.email = str(datos.get("email", existente.email))
        self._repo_estudiantes.actualizar(existente)
        return existente

    def eliminar_estudiante(self, cedula: str) -> bool:
        return self._repo_estudiantes.eliminar(cedula)

    def listar_estudiantes(self) -> list[Estudiante]:
        return self._repo_estudiantes.obtener_todos()

    def buscar_estudiante(self, cedula: str) -> Estudiante | None:
        return self._repo_estudiantes.buscar_por_cedula(cedula)

    def registrar_materia(self, codigo: str, nombre: str, creditos: int = 3) -> Materia:
        if self._repo_materias.buscar_por_codigo(codigo):
            raise ValueError(f"Ya existe la materia con código {codigo}.")
        materia = Materia(codigo, nombre, creditos)
        self._repo_materias.guardar(materia)
        return materia

    def listar_materias(self) -> list[Materia]:
        return self._repo_materias.obtener_todas()

    def listar_docentes(self) -> list[Docente]:
        if self._repo_docentes is None:
            return []
        return self._repo_docentes.obtener_todos()

    def buscar_docente(self, cedula: str) -> Docente | None:
        if self._repo_docentes is None:
            return None
        return self._repo_docentes.buscar_por_cedula(cedula)

    def asignar_materia_a_estudiante(self, cedula: str, nombre_materia: str) -> None:
        estudiante = self._repo_estudiantes.buscar_por_cedula(cedula)
        if estudiante is None:
            raise KeyError(f"No existe estudiante con cédula {cedula}.")
        estudiante.asignar_materia(nombre_materia)
        self._repo_estudiantes.actualizar(estudiante)

    def registrar_calificacion(self, cedula: str, materia: str, nota: float) -> None:
        estudiante = self._repo_estudiantes.buscar_por_cedula(cedula)
        if estudiante is None:
            raise KeyError(f"No existe estudiante con cédula {cedula}.")
        estudiante.registrar_calificacion(materia, nota)
        self._repo_estudiantes.actualizar(estudiante)

    def importar_estudiantes_excel(self, ruta: str) -> int:
        if self._importador is None:
            raise RuntimeError("No hay importador de Excel configurado.")
        importados = self._importador.importar(ruta)
        registrados = 0
        for estudiante in importados:
            if self._repo_estudiantes.buscar_por_cedula(estudiante.cedula):
                self._repo_estudiantes.actualizar(estudiante)
            else:
                self._repo_estudiantes.guardar(estudiante)
            registrados += 1
        return registrados

    def exportar_estudiantes_excel(self, ruta: str) -> int:
        if self._exportador is None:
            raise RuntimeError("No hay exportador de Excel configurado.")
        estudiantes = self._repo_estudiantes.obtener_todos()
        self._exportador.exportar(estudiantes, ruta)
        return len(estudiantes)

    def obtener_resumenes_personas(self, personas: list[Persona]) -> list[str]:
        """POLIMORFISMO: cada subclase de Persona implementa obtener_resumen()."""
        return [persona.obtener_resumen() for persona in personas]

    def resolver_nombre_materia(self, referencia: str) -> str:
        ref = referencia.strip()
        if not ref:
            return ref
        for materia in self._repo_materias.obtener_todas():
            if materia.codigo == ref.upper() or materia.nombre.lower() == ref.lower():
                return materia.nombre
        return ref

    def materias_activas_estudiante(self, estudiante: Estudiante) -> list[tuple[str, str, int | str]]:
        catalogo = {m.codigo: m for m in self._repo_materias.obtener_todas()}
        por_nombre = {m.nombre.lower(): m for m in catalogo.values()}
        referencias: set[str] = set(estudiante.materias) | set(estudiante.calificaciones.keys())

        activas: list[tuple[str, str, int | str]] = []
        vistos: set[str] = set()
        for ref in referencias:
            ref = ref.strip()
            if not ref:
                continue
            materia = catalogo.get(ref.upper()) or por_nombre.get(ref.lower())
            if materia:
                if materia.codigo in vistos:
                    continue
                vistos.add(materia.codigo)
                activas.append((materia.codigo, materia.nombre, materia.creditos))
            elif ref.lower() not in vistos:
                vistos.add(ref.lower())
                activas.append(("", ref, ""))
        return activas
