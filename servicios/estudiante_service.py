from modulos.servicios.json_service import JsonService


class EstudianteService:

    @staticmethod
    def obtener_todos():
        return JsonService.leer_json("estudiantes")

    @staticmethod
    def guardar(estudiante):

        datos = JsonService.leer_json("estudiantes")

        if any(
            e.get("cedula") == estudiante.get("cedula")
            for e in datos
        ):
            return False

        datos.append(estudiante)

        JsonService.guardar_json(
            "estudiantes",
            datos
        )

        return True

    @staticmethod
    def actualizar(id_estudiante, nuevos_datos):

        datos = JsonService.leer_json("estudiantes")

        for estudiante in datos:

            if estudiante["id"] == id_estudiante:

                estudiante.update(nuevos_datos)

        JsonService.guardar_json(
            "estudiantes",
            datos
        )

    @staticmethod
    def eliminar(id_estudiante):

        datos = JsonService.leer_json("estudiantes")

        datos = [
            e for e in datos
            if e["id"] != id_estudiante
        ]

        JsonService.guardar_json(
            "estudiantes",
            datos
        )