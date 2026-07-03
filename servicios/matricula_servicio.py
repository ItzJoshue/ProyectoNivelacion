from domain.entidades.aula import Aula
from domain.entidades.curso import Curso
from domain.entidades.matricula import Matricula
from domain.entidades.postulante import Postulante
from infraestructura.utilidades.almacenamiento import guardar_json, leer_json, nuevo_id


class MatriculaServicio:
    """Gestión de aulas, cursos, postulantes y matrículas (módulo rama Modulosss)."""

    def listar_aulas(self) -> list[Aula]:
        return [Aula.from_dict(d) for d in leer_json("aulas")]

    def guardar_aula(self, codigo: str, capacidad: int) -> Aula:
        aula = Aula(nuevo_id("AUL"), codigo, capacidad)
        datos = leer_json("aulas")
        datos.append(aula.to_dict())
        guardar_json("aulas", datos)
        return aula

    def listar_cursos(self) -> list[Curso]:
        return [Curso.from_dict(d) for d in leer_json("cursos")]

    def guardar_curso(self, nombre: str, carrera: str, cupos: int) -> Curso:
        curso = Curso(nuevo_id("CUR"), nombre, carrera, cupos)
        datos = leer_json("cursos")
        datos.append(curso.to_dict())
        guardar_json("cursos", datos)
        return curso

    def listar_postulantes(self) -> list[Postulante]:
        return [Postulante.from_dict(d) for d in leer_json("postulantes")]

    def guardar_postulante(
        self, nombre: str, cedula: str, carrera: str, puntaje: float, correo: str = ""
    ) -> Postulante:
        postulante = Postulante(nuevo_id("POS"), nombre, cedula, carrera, puntaje, correo)
        datos = leer_json("postulantes")
        datos.append(postulante.to_dict())
        guardar_json("postulantes", datos)
        return postulante

    def listar_matriculas(self) -> list[Matricula]:
        return [Matricula.from_dict(d) for d in leer_json("matriculas")]

    def matricular(self, cedula_estudiante: str, id_curso: str, id_aula: str) -> Matricula:
        matriculas = leer_json("matriculas")
        if any(
            m.get("cedula_estudiante", m.get("estudiante_id")) == cedula_estudiante
            and m.get("curso_id", m.get("id_curso")) == id_curso
            for m in matriculas
        ):
            raise ValueError("El estudiante ya está matriculado en ese curso.")

        cursos = leer_json("cursos")
        curso = next((c for c in cursos if c.get("id") == id_curso), None)
        if curso:
            cupos = int(curso.get("cupos", 0))
            ocupados = sum(
                1 for m in matriculas if m.get("curso_id", m.get("id_curso")) == id_curso
            )
            if ocupados >= cupos:
                raise ValueError("El curso no tiene cupos disponibles.")

        matricula = Matricula(nuevo_id("MAT"), cedula_estudiante, id_curso, id_aula)
        matriculas.append(matricula.to_dict())
        guardar_json("matriculas", matriculas)
        return matricula

    def matriculas_de_estudiante(self, cedula: str) -> list[Matricula]:
        return [m for m in self.listar_matriculas() if m.cedula_estudiante == cedula]

    def generar_reporte(self) -> str:
        estudiantes = leer_json("estudiantes")
        docentes = leer_json("docentes")
        aulas = leer_json("aulas")
        cursos = leer_json("cursos")
        postulantes = leer_json("postulantes")
        matriculas = leer_json("matriculas")

        lineas = [
            "===== REPORTE GENERAL ULEAM =====\n",
            f"Estudiantes:  {len(estudiantes)}",
            f"Docentes:     {len(docentes)}",
            f"Aulas:        {len(aulas)}",
            f"Cursos:       {len(cursos)}",
            f"Postulantes:  {len(postulantes)}",
            f"Matrículas:   {len(matriculas)}\n",
            "===== MATRÍCULAS =====",
        ]

        est_map = {e.get("cedula"): e.get("nombre", "") for e in estudiantes}
        cur_map = {c.get("id"): c.get("nombre", "") for c in cursos}
        aul_map = {a.get("id"): a.get("codigo", "") for a in aulas}

        if not matriculas:
            lineas.append("No hay matrículas registradas.")
        else:
            for m in matriculas:
                ced = m.get("cedula_estudiante", m.get("estudiante_id", ""))
                cid = m.get("curso_id", m.get("id_curso", ""))
                aid = m.get("aula_id", m.get("id_aula", ""))
                lineas.append(
                    f"- {est_map.get(ced, ced)} | {cur_map.get(cid, cid)} | Aula {aul_map.get(aid, aid)}"
                )
        return "\n".join(lineas)
