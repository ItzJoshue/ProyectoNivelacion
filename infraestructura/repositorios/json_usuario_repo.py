from domain.entidades.usuario import Usuario
from domain.interfaces.repositorio_usuario import IRepositorioUsuario
from infraestructura.utilidades.almacenamiento import guardar_json, leer_json


class RepositorioUsuarioJson(IRepositorioUsuario):
    ARCHIVO = "usuarios"

    def guardar(self, usuario: Usuario) -> None:
        datos = leer_json(self.ARCHIVO)
        serializado = usuario.to_dict()
        datos = [d for d in datos if d.get("cedula") != usuario.cedula]
        datos.append(serializado)
        guardar_json(self.ARCHIVO, datos)

    def buscar_por_cedula(self, cedula: str) -> Usuario | None:
        for dato in leer_json(self.ARCHIVO):
            if dato.get("cedula") == cedula.strip():
                return Usuario.from_dict(dato)
        return None

    def obtener_todos(self) -> list[Usuario]:
        return [Usuario.from_dict(d) for d in leer_json(self.ARCHIVO)]
