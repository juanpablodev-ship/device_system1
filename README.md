# device_systems v2.0

API REST para la gestion de usuarios, dispositivos y prestamos del sistema device_systems, construida con FastAPI, SQLAlchemy y Alembic.

## Instalacion

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Ejecucion del servidor

```bash
uvicorn app.main:app --reload
```

Servidor: `http://127.0.0.1:8000`
Swagger: `http://127.0.0.1:8000/docs`
ReDoc: `http://127.0.0.1:8000/redoc`

## Migraciones con Alembic

```bash
alembic revision --autogenerate -m "descripcion"
alembic upgrade head
alembic history
```

## Estructura

```
device_systems/
├── app/
│   ├── main.py
│   ├── database/
│   │   └── connection.py
│   ├── models/
│   │   ├── user_model.py
│   │   ├── device_model.py
│   │   └── loan_model.py
│   ├── schemas/
│   │   ├── user_schema.py
│   │   ├── device_schema.py
│   │   └── loan_schema.py
│   ├── routes/
│   │   ├── user_routes.py
│   │   ├── device_routes.py
│   │   └── loan_routes.py
│   ├── services/
│   │   ├── user_service.py
│   │   ├── device_service.py
│   │   └── loan_service.py
│   └── dependencies/
│       └── database_dependency.py
├── alembic/
│   └── versions/
├── alembic.ini
├── requirements.txt
└── README.md
```

## Endpoints

### Users

| Metodo | Ruta | Descripcion |
|--------|------|-------------|
| GET | `/users/` | Listar usuarios |
| GET | `/users/{id}` | Obtener usuario |
| POST | `/users/` | Crear usuario |
| PUT | `/users/{id}` | Actualizar usuario |
| PATCH | `/users/{id}` | Actualizar parcial |
| DELETE | `/users/{id}` | Eliminar usuario |

### Devices

| Metodo | Ruta | Descripcion |
|--------|------|-------------|
| GET | `/devices/` | Listar dispositivos |
| GET | `/devices/{id}` | Obtener dispositivo |
| POST | `/devices/` | Crear dispositivo |
| PUT | `/devices/{id}` | Actualizar dispositivo |
| PATCH | `/devices/{id}` | Actualizar parcial |
| DELETE | `/devices/{id}` | Eliminar dispositivo |

### Loans

| Metodo | Ruta | Descripcion |
|--------|------|-------------|
| GET | `/loans/` | Listar prestamos |
| GET | `/loans/{id}` | Obtener prestamo |
| POST | `/loans/` | Crear prestamo |
| PATCH | `/loans/{id}/return` | Devolver dispositivo |
| GET | `/loans/user/{user_id}` | Prestamos de usuario |
| GET | `/loans/device/{device_id}` | Historial de dispositivo |

## Modelos

### User
- id, name, email (unico), role, is_active, created_at

### Device
- id, name, serial_number (unico), device_type, brand, is_available, created_at

### Loan
- id, user_id (FK), device_id (FK), loan_date, return_date, status

## Relaciones

- User 1-N Loan
- Device 1-N Loan
- Loan N-1 User + Device

## Tecnologias

- Python 3, FastAPI, SQLAlchemy, Alembic, Pydantic v2, SQLite, Uvicorn
