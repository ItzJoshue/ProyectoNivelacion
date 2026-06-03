# =========================
# SISTEMA DE NIVELACION ULEAM
# =========================

#Clase Persona
class Persona:

    def __init__(self, nombre, cedula):
        self.nombre = nombre
        self.cedula = cedula

    def mostrar_datos(self):
        print("Nombre:", self.nombre)
        print("Cedula:", self.cedula)


#--------------------------
# Clase Profesor
#--------------------------

class Profesor(Persona):

    def __init__(self, nombre, cedula, materia):
        super().__init__(nombre, cedula)
        self.materia = materia

    def mostrar_profesor(self):
        self.mostrar_datos()
        print("Materia:", self.materia)


#--------------------------
# Clase Estudiante
#--------------------------

class Estudiante(Persona):

    def __init__(self, nombre, cedula, carrera):
        super().__init__(nombre, cedula)
        self.carrera = carrera

    def mostrar_estudiante(self):
        self.mostrar_datos()
        print("Carrera:", self.carrera)


#--------------------------
# Clase Aula
#--------------------------

class Aula:

    def __init__(self, numero, capacidad=30):
        self.numero = numero
        self.capacidad = capacidad

    def mostrar_aula(self):
        print("Numero de aula:", self.numero)
        print("Capacidad:", self.capacidad)


#--------------------------
# Clase Horario
#--------------------------

class Horario:

    def __init__(self, dia, hora):
        self.dia = dia
        self.hora = hora

    def mostrar_horario(self):
        print("Dia:", self.dia)
        print("Hora:", self.hora)


#--------------------------
# Clase CursoNivelacion
#--------------------------

class CursoNivelacion:

    def __init__(self, carrera, materia1, materia2):
        self.carrera = carrera
        self.materia1 = materia1
        self.materia2 = materia2

    def mostrar_curso(self):
        print("Carrera:", self.carrera)
        print("Materia 1:", self.materia1)
        print("Materia 2:", self.materia2)


#--------------------------
# Clase Inscripcion
#--------------------------

class Inscripcion:

    def __init__(self, estudiante, fecha="Sin fecha"):
        self.estudiante = estudiante
        self.fecha = fecha

    def mostrar_inscripcion(self):
        print("=== INSCRIPCION ===")
        self.estudiante.mostrar_estudiante()
        print("Fecha:", self.fecha)


#--------------------------
# Clase Matricula
#--------------------------

class Matricula:

    def __init__(self, estudiante, curso, aula):
        self.estudiante = estudiante
        self.curso = curso
        self.aula = aula

    def mostrar_matricula(self):
        print("=== MATRICULA ===")
        self.estudiante.mostrar_estudiante()
        self.curso.mostrar_curso()
        self.aula.mostrar_aula()


# =========================
# PRUEBAS DEL SISTEMA
# =========================

# Profesor
prof1 = Profesor("Jharol Mendoza", "1304567890", "Programacion Orientada a Objetos")

# Estudiante
est1 = Estudiante("Hotman Ortega", "1316213097", "Ingenieria en Software")

# Aula
aula1 = Aula("A-12")

# Horario
horario1 = Horario("Lunes", "08:00 AM")

# Curso de nivelacion
curso1 = CursoNivelacion(
    "Ingenieria en Software",
    "Programacion Orientada a Objetos",
    "Base de Datos"
)

# Inscripcion
ins1 = Inscripcion(est1, "10/05/2026")

# Matricula
mat1 = Matricula(est1, curso1, aula1)

#--------------------------
# MOSTRAR DATOS
#--------------------------

while True:

    print("\n===== MENU =====")
    print("1. Ver estudiante")
    print("2. Ver curso")
    print("3. Salir")

    opcion = input("Ingrese una opcion: ")

    if opcion == "1":
        est1.mostrar_estudiante()

    elif opcion == "2":
        curso1.mostrar_curso()

    elif opcion == "3":
        print("Saliendo...")
        break

    else:
        print("Opcion incorrecta")