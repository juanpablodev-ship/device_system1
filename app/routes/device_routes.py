from fastapi import APIRouter, Depends, Response
from typing import Optional
from sqlalchemy.orm import Session

from app.dependencies.database_dependency import get_db
from app.schemas.device_schema import DeviceCreate, DeviceUpdate, DevicePatch, DeviceResponse
from app.services import device_service

router = APIRouter(prefix="/devices", tags=["devices"])


@router.get("/", response_model=list[DeviceResponse], summary="Listar dispositivos", description="Obtiene la lista de todos los dispositivos, con filtros opcionales por tipo, disponibilidad, marca y busqueda.")
def get_devices(
    response: Response,
    device_type: Optional[str] = None,
    is_available: Optional[bool] = None,
    brand: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
):
    response.headers["X-App-Name"] = "device_systems"
    response.headers["X-API-Version"] = "2.0"
    return device_service.get_devices(db, device_type=device_type, is_available=is_available, brand=brand, search=search)


@router.get("/{device_id}", response_model=DeviceResponse, summary="Obtener dispositivo por ID", description="Obtiene los datos de un dispositivo especifico por su ID.")
def get_device(device_id: int, response: Response, db: Session = Depends(get_db)):
    response.headers["X-App-Name"] = "device_systems"
    response.headers["X-API-Version"] = "2.0"
    return device_service.get_device(db, device_id)


@router.post("/", response_model=DeviceResponse, status_code=201, summary="Crear dispositivo", description="Registra un nuevo dispositivo. El numero de serie debe ser unico.")
def create_device(device: DeviceCreate, response: Response, db: Session = Depends(get_db)):
    response.headers["X-App-Name"] = "device_systems"
    response.headers["X-API-Version"] = "2.0"
    return device_service.create_device(db, device)


@router.put("/{device_id}", response_model=DeviceResponse, summary="Actualizar dispositivo completo", description="Reemplaza todos los campos de un dispositivo existente.")
def update_device(device_id: int, device: DeviceUpdate, response: Response, db: Session = Depends(get_db)):
    response.headers["X-App-Name"] = "device_systems"
    response.headers["X-API-Version"] = "2.0"
    return device_service.update_device(db, device_id, device)


@router.patch("/{device_id}", response_model=DeviceResponse, summary="Actualizar dispositivo parcial", description="Actualiza solo los campos enviados de un dispositivo existente.")
def patch_device(device_id: int, device: DevicePatch, response: Response, db: Session = Depends(get_db)):
    response.headers["X-App-Name"] = "device_systems"
    response.headers["X-API-Version"] = "2.0"
    return device_service.patch_device(db, device_id, device)


@router.delete("/{device_id}", summary="Eliminar dispositivo", description="Elimina un dispositivo del sistema por su ID.", status_code=200)
def delete_device(device_id: int, response: Response, db: Session = Depends(get_db)):
    response.headers["X-App-Name"] = "device_systems"
    response.headers["X-API-Version"] = "2.0"
    return device_service.delete_device(db, device_id)
