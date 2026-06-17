from modulos.servicios.json_service import JsonService


class CursoService:

    @staticmethod
    def obtener_todos():
        return JsonService.leer_json("cursos")

    @staticmethod
    def buscar_por_id(id_curso):

        cursos = JsonService.leer_json("cursos")

        return next(
            (
                c for c in cursos
                if c["id"] == id_curso
            ),
            None
        )