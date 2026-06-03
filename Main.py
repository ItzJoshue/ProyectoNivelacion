from Modulos.personas import Profesor, Estudiante
from Modulos.infraestructura import Aula, Horario, Cronograma
from Modulos.universidad import CursoNivelacion, Matricula

# Almacenamiento temporal (Base de datos en memoria)
aulas = []
cursos = []
profesores = []
estudiantes = []
matriculas = []

# Configuración inicial del Cronograma
cronograma_uleam = Cronograma("Periodo Académico ULEAM 2026")

def buscar_estudiante(cedula):
    for est in estudiantes:
        if est.get_cedula() == cedula:
            return est
    return None

def buscar_aula(numero):
    for au in aulas:
        if au.get_numero() == numero:
            return au
    return None

def buscar_curso(carrera):
    for cur in cursos:
        if cur.get_carrera().lower() == carrera.lower():
            return cur
    return None

# ==========================================
# MENÚ PRINCIPAL INTERACTIVO
# ==========================================
while True:
    print("\n" + "="*40)
    print("      SISTEMA ACADÉMICO REAL ULEAM     ")
    print("="*40)
    print("1. [Configuración] Registrar Aula")
    print("2. [Configuración] Registrar Curso de Nivelación")
    print("3. [Configuración] Registrar Hito en Cronograma")
    print("4. [Docencia]      Registrar Profesor")
    print("5. [Admisiones]    Registrar Estudiante")
    print("6. [Admisiones]    Procesar Matrícula (Efectuar Herencia)")
    print("7. [Académico]     Subir Notas a Estudiante")
    print("8. [Reportes]      Ver Reporte de Matrícula Completa")
    print("9. [Reportes]      Ver Lista de Profesores")
    print("10.[Reportes]      Ver Cronograma Actual")
    print("0. Salir")
    print("="*40)

    opcion = input("Seleccione una opción: ")

    if opcion == "1":
        print("\n--- REGISTRO DE AULA ---")
        num = input("Número/Código del Aula (Ej: B-202): ")
        cap = int(input("Capacidad de alumnos: "))
        aulas.append(Aula(num, cap))
        print("✅ Aula registrada con éxito.")

    elif opcion == "2":
        print("\n--- REGISTRO DE CURSO DE NIVELACIÓN ---")
        carrera = input("Carrera a la que pertenece el curso: ")
        m1 = input("Nombre de la Materia 1: ")
        m2 = input("Nombre de la Materia 2: ")
        cursos.append(CursoNivelacion(carrera, m1, m2))
        print(f"✅ Curso de Nivelación para '{carrera}' creado.")

    elif opcion == "3":
        print("\n--- AGREGAR HITO AL CRONOGRAMA ---")
        fecha = input("Fecha (AAAA-MM-DD): ")
        evento = input("Evento académico: ")
        cronograma_uleam.agregar_hito(fecha, evento)
        print("✅ Evento indexado al cronograma.")

    elif opcion == "4":
        print("\n--- REGISTRO DE PROFESOR ---")
        if not aulas:
            print("❌ Error: Debe registrar al menos un aula antes de asignar un profesor.")
            continue
        nom = input("Nombre completo del Profesor: ")
        ced = input("Cédula de identidad: ")
        mat = input("Materia que dicta: ")
        
        print("\nAulas disponibles:")
        for au in aulas: print(f" - {au.get_numero()}")
        aula_sel = input("Escriba el código del aula asignada: ")
        obj_aula = buscar_aula(aula_sel)
        
        if not obj_aula:
            print("❌ Aula no encontrada. Cancelando registro.")
            continue
            
        dia = input("Días de clase (Ej: Lunes y Martes): ")
        hora = input("Horario (Ej: 08:00 - 10:00): ")
        obj_horario = Horario(dia, hora)
        
        profesores.append(Profesor(nom, ced, mat, obj_aula, obj_horario))
        print("Profesor registrado y asignado correctamente.")

    elif opcion == "5":
        print("\n--- REGISTRO DE ESTUDIANTE ---")
        nom = input("Nombre completo del Estudiante: ")
        ced = input("Cédula de identidad: ")
        carrera = input("Carrera asignada: ")
        estudiantes.append(Estudiante(nom, ced, carrera))
        print("Estudiante pre-registrado en el sistema.")

    elif opcion == "6":
        print("\n--- PROCESO DE MATRICULACIÓN ---")
        if not estudiantes or not cursos or not aulas:
            print("❌ Requisito: Deben existir Estudiantes, Cursos y Aulas en el sistema.")
            continue
            
        ced_est = input("Ingrese la Cédula del estudiante a matricular: ")
        est = buscar_estudiante(ced_est)
        if not est:
            print("❌ Estudiante no encontrado.")
            continue
            
        cur = buscar_curso(est.get_carrera())
        if not cur:
            print(f"❌ No existe un Curso de Nivelación configurado para la carrera: {est.get_carrera()}")
            continue

        print("\nAulas disponibles:")
        for au in aulas: print(f" - {au.get_numero()}")
        aula_sel = input("Asigne un aula para la matrícula: ")
        obj_aula = buscar_aula(aula_sel)
        
        if not obj_aula:
            print("❌ Aula no válida.")
            continue
            
        f_mat = input("Fecha de Matrícula (DD/MM/AAAA): ")
        
        # Guardamos la matrícula que internamente inicializa la inscripción mediante super()
        matriculas.append(Matricula(est, cur, obj_aula, f_mat))
        print(f"✅ ¡Estudiante matriculado con éxito en {est.get_carrera()}!")

    elif opcion == "7":
        print("\n--- SUBIR CALIFICACIONES ---")
        ced_est = input("Cédula del estudiante: ")
        est = buscar_estudiante(ced_est)
        if not est:
            print("❌ Estudiante no encontrado.")
            continue
            
        cur = buscar_curso(est.get_carrera())
        if not cur:
            print("❌ El estudiante no cuenta con un esquema de curso.")
            continue
            
        print(f"Materias de su plan:")
        materias = cur.get_materias()
        for idx, m in enumerate(materias, 1):
            print(f"{idx}. {m}")
            
        sel_m = int(input("Seleccione el número de materia a calificar: ")) - 1
        if 0 <= sel_m < len(materias):
            nota = float(input(f"Ingrese la nota para '{materias[sel_m]}' (0.0 - 10.0): "))
            est.registrar_nota(materias[sel_m], nota)
            print("✅ Nota asentada en el sistema.")
        else:
            print("❌ Selección inválida.")

    elif opcion == "8":
        print("\n--- REPORTE GENERAL DE MATRÍCULAS ---")
        if not matriculas:
            print("No existen matrículas procesadas en este periodo.")
        for mat in matriculas:
            mat.mostrar_matricula_completa()

    elif opcion == "9":
        if not profesores:
            print("No hay profesores registrados.")
        for prof in profesores:
            prof.mostrar_profesor()

    elif opcion == "10":
        cronograma_uleam.mostrar_cronograma()

    elif opcion == "0":
        print("Saliendo del ecosistema informático ULEAM...")
        break
    else:
        print("❌ Opción inválida.")