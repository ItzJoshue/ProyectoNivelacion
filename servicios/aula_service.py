from modulos.servicios.json_service import JsonService


class AulaService:

    @staticmethod
    def obtener_todos():
        return JsonService.leer_json("aulas")

    @staticmethod
    def guardar(aula):

        datos = JsonService.leer_json("aulas")
        datos.append(aula)

        JsonService.guardar_json(
            "aulas",
            datos
        )

    @staticmethod
    def eliminar(id_aula):

        datos = JsonService.leer_json("aulas")

        datos = [
            a for a in datos
            if a["id"] != id_aula
        ]

        JsonService.guardar_json(
            "aulas",
            datos
        )