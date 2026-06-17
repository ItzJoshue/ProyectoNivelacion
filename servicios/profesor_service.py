from modulos.servicios.json_service import JsonService


class ProfesorService:

    @staticmethod
    def obtener_todos():
        return JsonService.leer_json("profesores")

    @staticmethod
    def guardar(profesor):

        datos = JsonService.leer_json("profesores")
        datos.append(profesor)

        JsonService.guardar_json(
            "profesores",
            datos
        )

    @staticmethod
    def actualizar(id_profesor, datos_nuevos):

        datos = JsonService.leer_json("profesores")

        for profesor in datos:

            if profesor["id"] == id_profesor:
                profesor.update(datos_nuevos)

        JsonService.guardar_json(
            "profesores",
            datos
        )

    @staticmethod
    def eliminar(id_profesor):

        datos = JsonService.leer_json("profesores")

        datos = [
            p for p in datos
            if p["id"] != id_profesor
        ]

        JsonService.guardar_json(
            "profesores",
            datos
        )