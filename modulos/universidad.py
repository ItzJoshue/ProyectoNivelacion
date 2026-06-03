from personas import Estudiante

class CursoNivelacion:
    def __init__(self, carrera, materia1, materia2):
        self.__carrera = carrera
        self.__materia1 = materia1
        self.__materia2 = materia2

    def get_carrera(self): return self.__carrera
    def get_materias(self): return [self.__materia1, self.__materia2]

    def mostrar_curso(self):
        print(f"Curso de Nivelación: {self.__carrera}")
        print(f" - Materia 1: {self.__materia1}")
        print(f" - Materia 2: {self.__materia2}")

class Matricula():
    def __init__(self, estudiante: Estudiante, curso: CursoNivelacion, aula, fecha_inscripcion, fecha_matricula):
        super().__init__(estudiante, fecha_inscripcion)
        self.__curso = curso
        self.__aula = aula
        self.__fecha_matricula = fecha_matricula

    def get_curso(self): return self.__curso
    def get_aula(self): return self.__aula
    def get_fecha_matricula(self): return self.__fecha_matricula

    def mostrar_matricula_completa(self):
        print("\n==================================================")
        print("       REPORTE COMPLETO DE MATRÍCULA - ULEAM      ")
        print("==================================================")
        print(f"ID Estudiante:    {self._estudiante.get_id_estudiante()}")
        print(f"Nombre:           {self._estudiante.get_nombre()}")
        print(f"Cédula:           {self._estudiante.get_cedula()}")
        print(f"Carrera:          {self._estudiante.get_carrera()}")
        print(f"F. Inscripción:   {self.get_fecha_inscripcion()}")
        print(f"F. Matriculación: {self.get_fecha_matricula()}")
        print("--------------------------------------------------")
        
        # Validación y despliegue de Materias y Notas
        materias = self.__curso.get_materias() if self.__curso else []
        notas_estudiante = self._estudiante.get_notas()
        
        if materias:
            print("Materias Cursando y Calificaciones:")
            for mat in materias:
                # Si no tiene nota asignada todavía, muestra "Sin nota"
                nota = exam if (exam := notas_estudiante.get(mat)) is not None else "Sin nota"
                print(f"  • {mat.ljust(35)} -> Nota: {nota}")
        else:
            print("Materias asignadas: Ninguna")
            
        print("--------------------------------------------------")
        print(f"Aula Asignada:    {self.__aula.get_numero()}")
        print("==================================================\n")