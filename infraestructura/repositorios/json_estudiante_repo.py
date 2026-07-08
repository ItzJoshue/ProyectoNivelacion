from domain.entidades.estudiante import Estudiante
from domain.interfaces.repositorio import IRepositorioEstudiante
from infraestructura.utilidades.almacenamiento import guardar_json, leer_json


class RepositorioEstudianteJson(IRepositorioEstudiante):
    """
    POLIMORFISMO CON INTERFACES: implementación concreta del contrato IRepositorioEstudiante.
    Persiste objetos Estudiante en archivos JSON sin que el servicio conozca el detalle.
    """

    ARCHIVO = "estudiantes"

    def guardar(self, estudiante: Estudiante) -> None:
        datos = leer_json(self.ARCHIVO)
        serializado = estudiante.to_dict()
        datos = [d for d in datos if d.get("cedula") != estudiante.cedula]
        datos.append(serializado)
        guardar_json(self.ARCHIVO, datos)

    def obtener_todos(self) -> list[Estudiante]:
        return [Estudiante.from_dict(d) for d in leer_json(self.ARCHIVO)]

    def buscar_por_cedula(self, cedula: str) -> Estudiante | None:
        for dato in leer_json(self.ARCHIVO):
            if dato.get("cedula") == cedula.strip():
                return Estudiante.from_dict(dato)
        return None

    def eliminar(self, cedula: str) -> bool:
        datos = leer_json(self.ARCHIVO)
        filtrados = [d for d in datos if d.get("cedula") != cedula.strip()]
        if len(filtrados) == len(datos):
            return False
        guardar_json(self.ARCHIVO, filtrados)
        return True

    def actualizar(self, estudiante: Estudiante) -> None:
        if self.buscar_por_cedula(estudiante.cedula) is None:
            raise KeyError(f"No existe estudiante con cédula {estudiante.cedula}.")
        self.guardar(estudiante)
