from domain.entidades.docente import Docente
from domain.interfaces.repositorio_docente import IRepositorioDocente
from infraestructura.utilidades.almacenamiento import guardar_json, leer_json


class RepositorioDocenteJson(IRepositorioDocente):
    ARCHIVO = "docentes"

    def guardar(self, docente: Docente) -> None:
        datos = leer_json(self.ARCHIVO)
        serializado = docente.to_dict()
        datos = [d for d in datos if d.get("cedula") != docente.cedula]
        datos.append(serializado)
        guardar_json(self.ARCHIVO, datos)

    def obtener_todos(self) -> list[Docente]:
        return [Docente.from_dict(d) for d in leer_json(self.ARCHIVO)]

    def buscar_por_cedula(self, cedula: str) -> Docente | None:
        for dato in leer_json(self.ARCHIVO):
            if dato.get("cedula") == cedula.strip():
                return Docente.from_dict(dato)
        return None

    def eliminar(self, cedula: str) -> bool:
        datos = leer_json(self.ARCHIVO)
        filtrados = [d for d in datos if d.get("cedula") != cedula.strip()]
        if len(filtrados) == len(datos):
            return False
        guardar_json(self.ARCHIVO, filtrados)
        return True

    def actualizar(self, docente: Docente) -> None:
        if self.buscar_por_cedula(docente.cedula) is None:
            raise KeyError(f"No existe docente con cédula {docente.cedula}.")
        self.guardar(docente)
