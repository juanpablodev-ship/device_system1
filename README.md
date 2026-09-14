# Nexus Workforce API v3

Microservicio para administración de personal organizacional, diseñado con arquitectura en capas y patrón de gestor de dominio.

## Qué es esto

Nexus Workforce expone una API HTTP que permite realizar operaciones CRUD completas sobre registros de personal: altas, consultas con filtros, reemplazos totales, ajustes parciales y bajas. La información se almacena en SQLite a través de SQLAlchemy ORM.

## Tecnologías

- Python 3.11+
- FastAPI con lifespan management
- SQLAlchemy (síncrono, SQLite)
- Pydantic v2 + pydantic-settings
- Middleware personalizado de timing

## Cómo arrancar

```bash
pip install -r requirements.txt
uvicorn core.app:application --reload
```

Documentación interactiva disponible en `/docs` (Swagger) y `/redoc`.

## Arquitectura

```
core/
├── config.py        # Configuración centralizada con pydantic-settings
├── app.py           # Factory de la app, lifespan, middlewares, handlers
├── database.py      # Engine SQLAlchemy y factoría de sesiones
├── exceptions.py    # Excepciones de dominio con códigos propios
└── middleware.py     # Middleware de medición de tiempo de respuesta

models/
└── staff.py         # Modelo ORM (tabla staff)

schemas/
└── staff.py         # DTOs de entrada/salida con validaciones

crud/
└── staff.py         # Clase GestorPersonal — toda la lógica de negocio

api/v1/
├── router.py        # Router aggregador de la versión 1
└── staff.py         # Endpoints REST del recurso personal
```

## Endpoints

Método | Ruta | Descripción | Status
-------|------|-------------|-------
GET | `/api/v1/personal` | Listar plantilla (filtros: rol, activo) | 200
GET | `/api/v1/personal/{uid}` | Buscar por identificador | 200
POST | `/api/v1/personal` | Alta nuevo registro | 201
PUT | `/api/v1/personal/{uid}` | Reemplazo completo | 200
PATCH | `/api/v1/personal/{uid}` | Ajuste parcial | 200
DELETE | `/api/v1/personal/{uid}` | Baja definitiva | 204

## Códigos de error

Código HTTP | Significado
-----------|------------
409 | Registro duplicado (correo ya registrado)
404 | Registro no encontrado
422 | Cuerpo de petición vacío o error de validación

## Modelo de datos

Campo | Tipo | Descripción
------|------|-----------
uid | int | Identificador autoincremental
nombre_completo | str | Nombre completo (mín. 2 caracteres)
correo | str | Correo electrónico único
rol | enum | coordinador / operativo / practicante
activo | bool | Estado de alta (default: true)
fecha_alta | datetime | Fecha de incorporación
notas | str | Observaciones opcionales

## Endpoints de sistema

Ruta | Descripción
-----|------------
GET `/ping` | Healthcheck — devuelve `{"reply": "pong"}`
