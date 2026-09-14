# Talent Hub API

Servicio REST para la gestión de miembros de un equipo, construido con **FastAPI** y **SQLAlchemy**.

---

## Descripción general

Talent Hub expone una interfaz HTTP para administrar el ciclo de vida de los miembros de una organización: altas, consultas, filtros, modificaciones y bajas. La información se persiste en una base de datos SQLite mediante SQLAlchemy ORM.

---

## Stack tecnológico

| Componente       | Versión     |
|------------------|-------------|
| Python           | 3.11+       |
| FastAPI          | latest      |
| Pydantic         | v2          |
| SQLAlchemy       | latest      |
| Uvicorn          | latest      |
| email-validator  | latest      |

---

## Estructura del proyecto

```
src/
├── app.py                  # Punto de entrada de la aplicación
├── endpoints/
│   └── member_endpoints.py # Definición de rutas HTTP
├── logic/
│   └── member_logic.py     # Reglas de negocio y operaciones CRUD
├── dto/
│   └── member_dto.py       # Modelos de transferencia de datos
├── entities/
│   ├── __init__.py
│   └── member_entity.py    # Modelo ORM (tabla members)
├── persistence/
│   └── engine.py           # Configuración de la base de datos
├── injectors/
│   ├── session_injector.py # Inyección de sesiones DB
│   └── header_injector.py  # Inyección de cabeceras HTTP
└── storage/
    └── memory_store.py     # Almacenamiento temporal en memoria
```

---

## Endpoints disponibles

### Miembros (`/members`)

| Método   | Ruta                    | Descripción                       | Código de éxito |
|----------|-------------------------|-----------------------------------|-----------------|
| `GET`    | `/members`              | Listar todos los miembros         | 200             |
| `GET`    | `/members/{id}`         | Buscar miembro por ID             | 200             |
| `POST`   | `/members`              | Registrar nuevo miembro           | 201             |
| `PUT`    | `/members/{id}`         | Actualización completa            | 200             |
| `PATCH`  | `/members/{id}`         | Actualización parcial             | 200             |
| `DELETE` | `/members/{id}`         | Eliminar miembro                  | 204             |

### Parámetros de filtrado (GET `/members`)

| Parámetro      | Tipo     | Valores permitidos           | Descripción              |
|----------------|----------|------------------------------|--------------------------|
| `position`     | string   | `manager`, `staff`, `intern` | Filtrar por posición     |
| `is_available` | boolean  | `true`, `false`              | Filtrar por disponibilidad |
| `sort_by`      | string   | `full_name`, `joined_on`     | Campo de ordenamiento    |

### Códigos de error

| Código | Significado                     |
|--------|---------------------------------|
| 400    | Correo duplicado o body vacío   |
| 404    | Miembro no encontrado           |
| 422    | Error de validación Pydantic    |

---

## Inicio rápido

### 1. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 2. Ejecutar el servidor

```bash
uvicorn src.app:application --reload
```

### 3. Acceder a la documentación

- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## Validaciones implementadas

| Campo            | Regla                                         |
|------------------|-----------------------------------------------|
| `full_name`      | Mínimo 3 caracteres                           |
| `contact_email`  | Formato de correo válido (email-validator)     |
| `position`       | Solo valores del enum: manager, staff, intern  |
| `is_available`   | Booleano (default: `true`)                     |

---

## Ejemplos de uso

### Registrar un miembro

```bash
curl -X POST http://localhost:8000/members \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "María García",
    "contact_email": "maria@talenthub.io",
    "position": "manager",
    "is_available": true
  }'
```

### Listar miembros disponibles

```bash
curl http://localhost:8000/members?is_available=true
```

### Filtrar por posición

```bash
curl http://localhost:8000/members?position=staff
```

### Actualizar parcialmente

```bash
curl -X PATCH http://localhost:8000/members/1 \
  -H "Content-Type: application/json" \
  -d '{"position": "manager"}'
```

### Eliminar un miembro

```bash
curl -X DELETE http://localhost:8000/members/1
```

---

## Licencia

MIT License
