from openpyxl import Workbook
from openpyxl.styles import Font

from domain.entidades.estudiante import Estudiante
from domain.interfaces.exportador import IExportadorEstudiantes


class ExcelExportadorEstudiantes(IExportadorEstudiantes):
    """Exporta estudiantes a un archivo Excel (.xlsx)."""

    ENCABEZADOS = ("cedula", "nombre", "apellido", "carrera", "email", "promedio")

    def exportar(self, estudiantes: list[Estudiante], ruta: str) -> None:
        libro = Workbook()
        hoja = libro.active
        hoja.title = "Estudiantes"

        hoja.append(list(self.ENCABEZADOS))
        for celda in hoja[1]:
            celda.font = Font(bold=True)

        for estudiante in estudiantes:
            datos = estudiante.to_dict()
            hoja.append([datos[col] for col in self.ENCABEZADOS])

        for columna in hoja.columns:
            longitud = max(len(str(celda.value or "")) for celda in columna)
            hoja.column_dimensions[columna[0].column_letter].width = min(longitud + 2, 40)

        libro.save(ruta)
