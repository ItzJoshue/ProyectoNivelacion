from openpyxl import Workbook
from openpyxl.styles import Font

from domain.entidades.estudiante import Estudiante
from domain.interfaces.exportador import IExportadorEstudiantes


class ExcelExportadorEstudiantes(IExportadorEstudiantes):
    """
    Abstracción orientada a objetos para la salida de datos .
    
    Garantiza una Alta Cohesión al centralizar los formatos de estilo
    y anchos adaptativos en métodos de única responsabilidad
    """

    # Encapsulamiento de metadatos del reporte mediante constantes privadas de clase
    _TITULOS_CABECERA = ("Cédula", "Nombre", "Apellido", "Carrera", "Email", "Promedio")

    def exportar(self, estudiantes: list[Estudiante], ruta: str) -> None:
        """
        Plantilla metodológica estructural que delega la construcción del archivo 
        interactuando con la interfaz pública del dominio.
        """
        libro = Workbook()
        hoja = libro.active
        hoja.title = "Estudiantes"

        self._escribir_cabeceras_con_estilo(hoja)
        self._escribir_coleccion_estudiantes(hoja, estudiantes)
        self._aplicar_dimensionamiento_adaptativo(hoja)

        libro.save(ruta)

    def _escribir_cabeceras_con_estilo(self, hoja) -> None:
        """Aplica el encapsulamiento de estilos visuales sobre la primera fila."""
        hoja.append(list(self._TITULOS_CABECERA))
        fuente_negrita = Font(bold=True, name="Arial", size=11)
        
        for celda in hoja[1]:
            celda.font = fuente_negrita

    def _escribir_coleccion_estudiantes(self, hoja, estudiantes: list[Estudiante]) -> None:
        """
        Paso de Mensajes (Unidad 1): Invoca el estado del objeto Estudiante de forma explícita.
        
        Evita el acoplamiento a diccionarios planos o desestructuraciones mutables.
        """
        for estudiante in estudiantes:
            # Consumo directo de los getters/propiedades de la entidad protegida
            registro_datos = [
                estudiante.cedula,
                estudiante.nombre,
                estudiante.apellido,
                estudiante.carrera,
                estudiante.email,
                getattr(estudiante, "promedio", 0.0)
            ]
            hoja.append(registro_datos)

    def _aplicar_dimensionamiento_adaptativo(self, hoja) -> None:
        """Algoritmo de cálculo encapsulado para el ancho proporcional de las celdas."""
        for columna in hoja.columns:
            # Determinación polimórfica de longitud basada en strings
            longitud_maxima = max(len(str(celda.value or "")) for celda in columna)
            letra_columna = columna[0].column_letter
            
            # Encapsula el límite máximo de crecimiento de las celdas (Invariante visual)
            hoja.column_dimensions[letra_columna].width = min(longitud_maxima + 3, 45)
