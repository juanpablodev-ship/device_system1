from fastapi import FastAPI
from src.persistence.engine import Base, engine
from src.entities.member_entity import Member
from src.endpoints import member_endpoints

Base.metadata.create_all(bind=engine)

group_tags = [
    {
        "name": "Members",
        "description": "ABM completo del recurso **miembros**. "
                       "Permite registrar, consultar, filtrar, actualizar y eliminar.",
    },
    {
        "name": "Health",
        "description": "Endpoint de verificación del estado del servicio.",
    },
]

application = FastAPI(
    title="Talent Hub API",
    description="""
API REST para la **gestión de talento** de la plataforma Talent Hub.

## Capacidades
- 📋 Listado y filtrado de miembros por posición y estado
- 👤 Búsqueda individual por identificador
- ➕ Registro de nuevos miembros con validación
- ✏️ Actualización total vía **PUT**
- 🔧 Actualización selectiva vía **PATCH**
- 🗑️ Baja de miembros vía **DELETE**

## Documentación
- **Swagger UI** → `/docs`
- **ReDoc** → `/redoc`

    """,
    version="1.0.0",
    contact={
        "name": "Talent Hub",
        "email": "info@talenthub.io",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
    openapi_tags=group_tags,
)

application.include_router(member_endpoints.router)


@application.get("/", tags=["Health"], summary="Verificar estado del servicio")
def health_check():
    return {
        "status": "operational",
        "service": "Talent Hub API v1.0.0",
        "documentation": "/docs",
    }
