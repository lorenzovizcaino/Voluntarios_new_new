# Sistema de Gestión de Voluntariado

## Descripción del Proyecto

Aplicación integral de gestión de voluntariado diseñada para optimizar la coordinación y asignación de tareas para asociaciones de voluntarios. El sistema cuenta con un enfoque de doble cuenta con funcionalidades separadas para administradores y voluntarios.

## Características Principales

### Módulo de Administración
- Gestión de Tareas:
  - Crear, editar y eliminar tareas
  - Especificar detalles de tareas: nombre, ubicación, fecha, turno, voluntarios necesarios
  - Sistema de asignación manual y automática de voluntarios
  <p align="center">
    <img src="/images_md/admin1.png" width="600" alt="Captura modo administrador 1">
  </p>

  <p align="center">
    <img src="/images_md/admin2.png" width="600" alt="Captura modo administrador 2">
  </p>

  <p align="center">
    <img src="/images_md/admin3.png" width="600" alt="Captura modo administrador 3">
  </p>

### Interfaz de Usuario de Voluntarios
- Panel de Control de Tareas Asignadas
- Calendarios de Disponibilidad:
  - Disponibilidad diaria
  - Selección de disponibilidad semanal
  - Selección de turno mensual
  
  <p align="center">
    <img src="/images_md/user_tareas.png" width="600" alt="Captura modo usuario 1">
  </p>

  <p align="center">
    <img src="/images_md/user_calendario_por_dia.png" width="600" alt="Captura modo usuario 2">
  </p>

  <p align="center">
    <img src="/images_md/user_calendario_por_turno.png" width="600" alt="Captura modo usuario 3">
  </p>

  <p align="center">
    <img src="/images_md/user_calendario_por_semana.png" width="600" alt="Captura modo usuario 4">
  </p>

### Notificaciones Automáticas con Telegram
Característica destacada: Notificaciones personalizadas con n8n

- Automatización de recordatorios de tareas
- Notificaciones enviadas un día antes de la tarea programada
- Integración con Telegram para comunicaciones instantáneas
- Los voluntarios pueden optar por recibir o no estas notificaciones

#### Cómo Funcionan las Notificaciones
1. El sistema genera un listado de tareas próximas
2. n8n procesa la información y programa las notificaciones
3. Se envía un mensaje personalizado a través de Telegram
4. El voluntario recibe un recordatorio con detalles de la tarea

#### Beneficios
- Reducción del olvido de tareas
- Comunicación proactiva
- Mayor compromiso de los voluntarios
- Flexibilidad para el usuario (se pueden activar o no)

## Stack Tecnológico
- **Lenguaje de Backend**: Python
- **Framework de API**: FastAPI
- **Framework de UI**: Flet (Multiplataforma)
- **Base de Datos**: SQLite
- **Contenedorización**: Docker
- **Automatización de Flujos**: N8N
- **Comunicación**: Telegram, Email, Notificaciones Windows

## Objetivos del Proyecto

- Centralizar información de voluntarios y tareas
- Automatizar sistemas de notificación
- Agilizar la coordinación de voluntarios
- Proporcionar gestión flexible de disponibilidad

## Motivaciones del Proyecto

- Eliminar procesos manuales propensos a errores
- Mejorar la eficiencia de comunicación
- Optimizar la asignación de recursos humanos
- Mejorar la experiencia de los voluntarios
  
## Despliegue

- Levantar el servicio con Docker (solo necesario para las notificaciones de Telegram)
- Ejecutar el archivo python app.py ubicado en el directorio frontend
  <p align="center">
    <img src="/images_md/login.png" width="300" alt="Captura del login">
  </p>
- Usuarios de prueba creados:
  - Administradores:
    - usuario: admin, password: admin
  - Voluntarios:
    - usuario: antonio, password: 123
    - usuario: remi, password: 123
    - usuario: antia, password: 123
    - usuario: user4, password: 123
    - usuario: user5, password: 123
  - Se adjuntan los archivos JSON necesarios para la automatización con n8n en la carpeta "json n8n"

## Hoja de Ruta Futura

- Arquitectura escalable
- Posibles mejoras de características
- Mejora continua de algoritmos de asignación

## Contribuidores

Manuel Antonio Lorenzo Vizcaíno

## Contacto

lorenzovizcaino@gmail.com
