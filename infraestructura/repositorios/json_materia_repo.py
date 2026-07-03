from domain.entidades.materia import Materia
from domain.interfaces.repositorio_materia import IRepositorioMateria
from infraestructura.utilidades.almacenamiento import guardar_json, leer_json


class RepositorioMateriaJson(IRepositorioMateria):
    ARCHIVO = "materias"

    def guardar(self, materia: Materia) -> None:
        datos = leer_json(self.ARCHIVO)
        serializado = {
            "codigo": materia.codigo,
            "nombre": materia.nombre,
            "creditos": materia.creditos,
        }
        datos = [d for d in datos if d.get("codigo") != materia.codigo]
        datos.append(serializado)
        guardar_json(self.ARCHIVO, datos)

    def obtener_todas(self) -> list[Materia]:
        return [
            Materia(d["codigo"], d["nombre"], int(d.get("creditos", 3)))
            for d in leer_json(self.ARCHIVO)
        ]

    def buscar_por_codigo(self, codigo: str) -> Materia | None:
        for dato in leer_json(self.ARCHIVO):
            if dato.get("codigo") == codigo.strip().upper():
                return Materia(dato["codigo"], dato["nombre"], int(dato.get("creditos", 3)))
        return None

    def eliminar(self, codigo: str) -> bool:
        datos = leer_json(self.ARCHIVO)
        filtrados = [d for d in datos if d.get("codigo") != codigo.strip().upper()]
        if len(filtrados) == len(datos):
            return False
        guardar_json(self.ARCHIVO, filtrados)
        return True
