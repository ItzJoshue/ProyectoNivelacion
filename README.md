# ProyectoNivelacion
# ULEAM Management System

## Descripción del Proyecto

**ULEAM Management System** es un sistema diseñado para optimizar la gestión académica del proceso de nivelación de la Universidad Laica Eloy Alfaro de Manabí (ULEAM).

El objetivo principal es centralizar y organizar la información académica de los estudiantes, permitiendo una administración eficiente de registros, materias y calificaciones. La plataforma busca facilitar el trabajo de docentes y estudiantes mediante un acceso rápido y seguro a la información académica.

## Problemática

Actualmente, la gestión de la información académica durante el proceso de nivelación presenta diversos inconvenientes, entre ellos:

* Manejo manual de información académica.
* Duplicidad o pérdida de registros.
* Dificultad para el seguimiento de calificaciones.
* Acceso limitado a la información por parte de estudiantes y docentes.
* Procesos administrativos lentos y propensos a errores.

La ausencia de un sistema centralizado afecta la eficiencia y el control del rendimiento académico.

## Alcance del Proyecto

El sistema se enfoca exclusivamente en la gestión académica de la nivelación, incluyendo:

* Registro y administración de estudiantes.
* Gestión de materias de nivelación.
* Asignación de materias a estudiantes.
* Registro y consulta de calificaciones.
* Consulta de información académica básica.

### Fuera del Alcance

Las siguientes funcionalidades no forman parte de esta versión:

* Pagos en línea.
* Integración con plataformas externas.
* Aplicaciones móviles.
* Gestión financiera o administrativa avanzada.

## Funcionalidades Principales

* Registro, edición y consulta de estudiantes.
* Administración de materias de nivelación.
* Asignación de materias a estudiantes.
* Registro y consulta de calificaciones.
* Búsquedas rápidas de información académica.
* Centralización de datos académicos en una única plataforma.

## Beneficios

* Mejor organización de la información académica.
* Reducción de errores en el manejo de datos.
* Acceso rápido y sencillo para estudiantes y docentes.
* Seguimiento eficiente del rendimiento académico.
* Optimización de los procesos administrativos.

## Metodología de Trabajo

El proyecto se desarrollará mediante trabajo colaborativo, asignando responsabilidades específicas a cada integrante del equipo, incluyendo desarrollo, documentación y coordinación.

La comunicación se mantendrá mediante reuniones periódicas y herramientas de colaboración, garantizando una participación equitativa y una adecuada coordinación durante todas las etapas del proyecto.

## Estructura del proyecto (main unificado)

```
ProyectoNivelacion/
├── Main.py
├── Datos/                    # Persistencia JSON (estudiantes, usuarios, aulas…)
├── domain/                   # Entidades POO + interfaces ABC
│   ├── entidades/
│   └── interfaces/
├── factories/                # Factory Method
├── infraestructura/          # Repositorios JSON, Excel, utilidades
├── servicios/                # Lógica de negocio + Facade + inyección de dependencias
└── Vistas/
    ├── autenticacion/        # Login y registro
    ├── paneles/              # Panel docente / panel estudiante
    └── frames/               # Vistas CRUD y reportes
```

Integra el código de la rama `Modulosss` (aulas, cursos, matrículas, postulantes, reportes) con la arquitectura POO/SOLID de `main`.

## Autenticación y roles

1. **Registrarse** como estudiante o docente (crea cuenta + perfil académico).
2. **Iniciar sesión** con cédula y contraseña.
3. **Panel Docente**: acceso completo (estudiantes, materias, calificaciones, aulas, cursos, postulantes, matrículas, reportes, Excel).
4. **Panel Estudiante**: solo ve su perfil, calificaciones y matrículas propias.

## Conceptos POO documentados en código

| Concepto | Ubicación |
|----------|-----------|
| Encapsulamiento + `@property` | `domain/entidades/` |
| Herencia + polimorfismo (ABC) | `domain/entidades/persona.py` |
| Factory Method (patrón creacional) | `factories/persona_factory.py` |
| Facade (patrón estructural) | `servicios/contenedor.py` → `ContenedorAplicacion` |
| Interfaces ABC (SOLID - I, D) | `domain/interfaces/` |
| Inyección de dependencias | `servicios/contenedor.py`, `servicios/gestor_academico.py` |
| Composition Root | `servicios/contenedor.py` → `crear_contenedor()` |

## Instalación y ejecución

```bash
pip install -r requirements.txt
python Main.py
```

## Importar / exportar estudiantes (Excel)

Disponible en el **Panel Docente → Estudiantes**. Columnas: `cedula`, `nombre`, `apellido`, `carrera`, `email`.

---

## Ejemplos de conceptos POO y patrones en el código

A continuación se muestra **un ejemplo de cada concepto** solicitado, con la ruta exacta donde se aplica en el proyecto.

### Fundamentos de POO

| Concepto | Ejemplo en el código | Ruta |
|----------|---------------------|------|
| Abstracción y diagramas de modelado | Capa de dominio que modela Persona, Estudiante, Docente y Materia con relaciones documentadas | `domain/entidades/__init__.py` |
| Clases, objetos y relaciones entre clases | Clase `Estudiante` asociada a materias y calificaciones; vinculada a `Usuario` por cédula | `domain/entidades/estudiante.py` |
| Encapsulamiento, propiedades, constructores, métodos y sobrecarga | Atributos privados `_cedula`, `@property`, constructor con `super()` y sobrecarga con `@singledispatchmethod` en `consultar_calificacion` | `domain/entidades/estudiante.py` |
| Definición de la herencia y aplicación | `Estudiante` y `Docente` heredan atributos y comportamiento de `Persona` | `domain/entidades/docente.py` |
| Polimorfismo con clases abstractas | Métodos abstractos `obtener_rol()` y `obtener_resumen()` redefinidos en cada subclase | `domain/entidades/persona.py` |
| Polimorfismo con interfaces | `RepositorioEstudianteJson` implementa el contrato `IRepositorioEstudiante` | `infraestructura/repositorios/json_estudiante_repo.py` |
| Inyección de dependencias | `GestorAcademico` recibe repositorios e importadores por constructor, sin instanciarlos | `servicios/gestor_academico.py` |

### Patrones de diseño

| Tipo | Patrón | Ejemplo en el código | Ruta |
|------|--------|---------------------|------|
| Creacional | Factory Method | `EstudianteFactory` y `DocenteFactory` crean el tipo correcto de `Persona` | `factories/persona_factory.py` |
| Estructural | Facade | `ContenedorAplicacion` unifica el acceso a todos los servicios de la aplicación | `servicios/contenedor.py` |
| Comportamiento | Strategy | `App._entrar()` elige `PanelDocente` o `PanelEstudiante` según el rol del usuario | `Vistas/app.py` |
