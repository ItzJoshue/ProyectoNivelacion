from modulos.servicios.json_service import JsonService


class MatriculaService:

    @staticmethod
    def matricular(
        estudiante_id,
        curso_id,
        aula_id
    ):

        matriculas = JsonService.leer_json(
            "matriculas"
        )

        if any(
            m["estudiante_id"] == estudiante_id
            and m["curso_id"] == curso_id
            for m in matriculas
        ):
            return False

        nueva = {
            "id": JsonService.nuevo_id("MAT"),
            "estudiante_id": estudiante_id,
            "curso_id": curso_id,
            "aula_id": aula_id
        }

        matriculas.append(nueva)

        JsonService.guardar_json(
            "matriculas",
            matriculas
        )

        return True