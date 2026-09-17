from fastapi import APIRouter, Depends, Response
from typing import Optional
from sqlalchemy.orm import Session

from app.dependencies.database_dependency import get_db
from app.schemas.user_schema import UserCreate, UserUpdate, UserPatch, UserResponse, Role
from app.services import user_service

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=list[UserResponse], summary="Listar usuarios", description="Obtiene la lista de todos los usuarios registrados, con filtros opcionales por rol, estado y busqueda.")
def get_users(
    response: Response,
    role: Optional[Role] = None,
    is_active: Optional[bool] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
):
    response.headers["X-App-Name"] = "device_systems"
    response.headers["X-API-Version"] = "2.0"
    return user_service.get_users(db, role=role, is_active=is_active, search=search)


@router.get("/{user_id}", response_model=UserResponse, summary="Obtener usuario por ID", description="Obtiene los datos de un usuario especifico por su ID.")
def get_user(user_id: int, response: Response, db: Session = Depends(get_db)):
    response.headers["X-App-Name"] = "device_systems"
    response.headers["X-API-Version"] = "2.0"
    return user_service.get_user(db, user_id)


@router.post("/", response_model=UserResponse, status_code=201, summary="Crear usuario", description="Registra un nuevo usuario en el sistema. El correo debe ser unico.")
def create_user(user: UserCreate, response: Response, db: Session = Depends(get_db)):
    response.headers["X-App-Name"] = "device_systems"
    response.headers["X-API-Version"] = "2.0"
    return user_service.create_user(db, user)


@router.put("/{user_id}", response_model=UserResponse, summary="Actualizar usuario completo", description="Reemplaza todos los campos de un usuario existente.")
def update_user(user_id: int, user: UserUpdate, response: Response, db: Session = Depends(get_db)):
    response.headers["X-App-Name"] = "device_systems"
    response.headers["X-API-Version"] = "2.0"
    return user_service.update_user(db, user_id, user)


@router.patch("/{user_id}", response_model=UserResponse, summary="Actualizar usuario parcial", description="Actualiza solo los campos enviados de un usuario existente.")
def patch_user(user_id: int, user: UserPatch, response: Response, db: Session = Depends(get_db)):
    response.headers["X-App-Name"] = "device_systems"
    response.headers["X-API-Version"] = "2.0"
    return user_service.patch_user(db, user_id, user)


@router.delete("/{user_id}", summary="Eliminar usuario", description="Elimina un usuario del sistema por su ID.", status_code=200)
def delete_user(user_id: int, response: Response, db: Session = Depends(get_db)):
    response.headers["X-App-Name"] = "device_systems"
    response.headers["X-API-Version"] = "2.0"
    return user_service.delete_user(db, user_id)
