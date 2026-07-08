# Diagrama UML — Patrón Facade
ContenedorAplicacion actúa como Facade: las Vistas (Login, Registro) 
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
