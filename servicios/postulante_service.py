from modulos.servicios.json_service import JsonService


class PostulanteService:

    @staticmethod
    def obtener_todos():
        return JsonService.leer_json("postulantes")