# Diagramas UML — Patrones de Diseño

## Facade

`ContenedorAplicacion` actúa como Facade: las Vistas (Login, Registro) 
solo interactúan con él, sin conocer los 3 servicios internos que coordina.

```mermaid
classDiagram
  class LoginFrame {
    +iniciar_sesion()
  }
  class RegistroFrame {
    +registrar()
  }
  class ContenedorAplicacion {
    <<Facade>>
    -_gestor: GestorAcademico
    -_autenticacion: AutenticacionServicio
    -_matricula: MatriculaServicio
    +gestor
    +autenticacion
    +matricula
    +iniciar_sesion(cedula, pass)
    +registrar_usuario(datos, pass, rol)
    +obtener_perfil_estudiante(cedula)
  }
  class GestorAcademico {
    +listar_estudiantes()
    +registrar_estudiante(datos)
  }
  class AutenticacionServicio {
    +registrar(datos, pass, rol)
    +iniciar_sesion(cedula, pass)
  }
  class MatriculaServicio {
    +listar_cursos()
    +matricular(cedula, curso, aula)
  }
  LoginFrame ..> ContenedorAplicacion : usa
  RegistroFrame ..> ContenedorAplicacion : usa
  ContenedorAplicacion --> GestorAcademico : coordina
  ContenedorAplicacion --> AutenticacionServicio : coordina
  ContenedorAplicacion --> MatriculaServicio : coordina
```

## Strategy

`App._entrar()` decide qué panel mostrar según el rol del usuario. 
`PanelDocente` y `PanelEstudiante` son estrategias intercambiables: 
comparten el mismo propósito (mostrar la interfaz principal) pero cada 
una implementa un comportamiento distinto según el rol.

```mermaid
classDiagram
  class App {
    -usuario_actual: Usuario
    +_entrar(usuario)
  }
  class PanelAcceso {
    <<interface>>
  }
  class PanelDocente {
    +acceso completo
  }
  class PanelEstudiante {
    +vista limitada
  }
  App ..> PanelAcceso : elige segun rol
  PanelAcceso <|.. PanelDocente
  PanelAcceso <|.. PanelEstudiante
```

## Factory Method

`PersonaFactoryCreator` selecciona la fábrica adecuada según el tipo de 
persona a crear. Cada fábrica concreta (`EstudianteFactory`, `DocenteFactory`) 
sabe construir su propio tipo, sin que el código cliente conozca los detalles.

```mermaid
classDiagram
  class PersonaFactoryCreator {
    -_fabricas: dict
    +obtener_fabrica(tipo)$
  }
  class PersonaFactory {
    <<abstract>>
    +crear(datos)*
  }
  class EstudianteFactory {
    +crear(datos) Estudiante
  }
  class DocenteFactory {
    +crear(datos) Docente
  }
  class Estudiante
  class Docente

  PersonaFactoryCreator ..> PersonaFactory : selecciona
  PersonaFactory <|-- EstudianteFactory
  PersonaFactory <|-- DocenteFactory
  EstudianteFactory ..> Estudiante : crea
  DocenteFactory ..> Docente : crea
```
