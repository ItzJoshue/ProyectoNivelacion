class Persona:
    def __init__(self, nombre, cedula):
        self.__nombre = nombre
        self.__cedula = cedula

    def get_nombre(self): return self.__nombre
    def get_cedula(self): return self.__cedula

    def mostrar_datos(self):
        print(f"Nombre: {self.__nombre}")
        print(f"Cédula: {self.__cedula}")


class Profesor(Persona):
    __contador_id = 0

    def __init__(self, nombre, cedula, materia, aula, horario):
        super().__init__(nombre, cedula)
        Profesor.__contador_id += 1
        self.__id_profesor = f"PROF-{Profesor.__contador_id}"
        self.__materia = materia
        self.__aula = aula        
        self.__horario = horario  

    def get_id_profesor(self): return self.__id_profesor
    def get_materia(self): return self.__materia

    def mostrar_profesor(self):
        print(f"\n=== DATOS PROFESOR ({self.__id_profesor}) ===")
        self.mostrar_datos()
        print(f"Materia que ejerce: {self.__materia}")
        self.__aula.mostrar_aula()
        self.__horario.mostrar_horario()


class Estudiante(Persona):
    __contador_id = 0

    def __init__(self, nombre, cedula, carrera):
        super().__init__(nombre, cedula)
        Estudiante.__contador_id += 1
        self.__id_estudiante = f"EST-{Estudiante.__contador_id}"
        self.__carrera = carrera
        self.__notas = {} 

    def get_id_estudiante(self): return self.__id_estudiante
    def get_carrera(self): return self.__carrera
    def get_notas(self): return self.__notas
    
    def registrar_nota(self, materia, nota):
        if 0 <= nota <= 10:
            self.__notas[materia] = nota
        else:
            print("❌ La nota debe estar entre 0 y 10.")

    def mostrar_estudiante(self):
        print(f"\n=== DATOS ESTUDIANTE ({self.__id_estudiante}) ===")
        self.mostrar_datos()
        print(f"Carrera: {self.__carrera}")