from modulos.servicios.json_service import JsonService


class ReporteService:

    @staticmethod
    def generar_resumen():

        return {
            "estudiantes":
                len(JsonService.leer_json("estudiantes")),

            "profesores":
                len(JsonService.leer_json("profesores")),

            "aulas":
                len(JsonService.leer_json("aulas")),

            "cursos":
                len(JsonService.leer_json("cursos")),

            "postulantes":
                len(JsonService.leer_json("postulantes")),

            "matriculas":
                len(JsonService.leer_json("matriculas"))
        }