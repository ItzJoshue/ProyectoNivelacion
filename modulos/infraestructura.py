class Aula:
    def __init__(self, numero, capacidad=30):
        self.__numero = numero
        self.__capacidad = capacidad

    def get_numero(self): return self.__numero
    def get_capacidad(self): return self.__capacidad

    def mostrar_aula(self):
        print(f"Aula: {self.__numero} (Capacidad: {self.__capacidad})")


class Horario:
    def __init__(self, dia, hora):
        self.__dia = dia
        self.__hora = hora

    def get_dia(self): return self.__dia
    def get_hora(self): return self.__hora

    def mostrar_horario(self):
        print(f"Horario: {self.__dia} -> {self.__hora}")


class Cronograma:
    def __init__(self, periodo_lectivo):
        self.__periodo_lectivo = periodo_lectivo
        self.__hitos = {}

    def agregar_hito(self, fecha, evento):
        self.__hitos[fecha] = evento

    def mostrar_cronograma(self):
        print(f"\n=== CRONOGRAMA ACADÉMICO ({self.__periodo_lectivo}) ===")
        for fecha, evento in sorted(self.__hitos.items()):
            print(f"📅 {fecha}: {evento}")
        print("=========================================")