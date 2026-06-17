from pathlib import Path
import json
import uuid


class JsonService:

    @staticmethod
    def obtener_carpeta_datos():
        home = Path.home()

        posibles = [
            home / "Documents" / "Sistema_ULEAM_JSON_DATA",
            home / "Documentos" / "Sistema_ULEAM_JSON_DATA",
            home / "Sistema_ULEAM_JSON_DATA",
            Path.cwd() / "Sistema_ULEAM_JSON_DATA"
        ]

        for carpeta in posibles:
            try:
                carpeta.mkdir(parents=True, exist_ok=True)

                prueba = carpeta / "prueba_escritura.txt"
                prueba.write_text("ok", encoding="utf-8")
                prueba.unlink(missing_ok=True)

                return carpeta

            except Exception:
                pass

        raise RuntimeError(
            "No se pudo crear una carpeta para guardar los datos JSON."
        )

    DATA_DIR = obtener_carpeta_datos.__func__()

    ARCHIVOS = {
        "estudiantes": DATA_DIR / "estudiantes.json",
        "profesores": DATA_DIR / "profesores.json",
        "aulas": DATA_DIR / "aulas.json",
        "cursos": DATA_DIR / "cursos.json",
        "postulantes": DATA_DIR / "postulantes.json",
        "matriculas": DATA_DIR / "matriculas.json",
    }

    @staticmethod
    def iniciar_json():

        for ruta in JsonService.ARCHIVOS.values():

            ruta.parent.mkdir(parents=True, exist_ok=True)

            if not ruta.exists():
                ruta.write_text("[]", encoding="utf-8")

    @staticmethod
    def leer_json(nombre):

        ruta = JsonService.ARCHIVOS[nombre]

        try:

            if not ruta.exists():
                ruta.write_text("[]", encoding="utf-8")

            texto = ruta.read_text(encoding="utf-8").strip()

            if not texto:
                return []

            datos = json.loads(texto)

            return datos if isinstance(datos, list) else []

        except Exception:
            return []

    @staticmethod
    def guardar_json(nombre, datos):

        ruta = JsonService.ARCHIVOS[nombre]

        with open(ruta, "w", encoding="utf-8") as archivo:
            json.dump(
                datos,
                archivo,
                indent=4,
                ensure_ascii=False
            )

    @staticmethod
    def nuevo_id(prefijo):

        return f"{prefijo}-{uuid.uuid4().hex[:6].upper()}"