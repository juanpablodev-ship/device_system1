from sqlalchemy.orm import Session
from sqlalchemy import or_
from fastapi import HTTPException

from app.models.device_model import Device
from app.schemas.device_schema import DeviceCreate, DeviceUpdate, DevicePatch


def get_devices(db: Session, device_type: str = None, is_available: bool = None, brand: str = None, search: str = None):
    query = db.query(Device)
    if device_type:
        query = query.filter(Device.device_type == device_type)
    if is_available is not None:
        query = query.filter(Device.is_available == is_available)
    if brand:
        query = query.filter(Device.brand.ilike(f"%{brand}%"))
    if search:
        query = query.filter(
            or_(
                Device.name.ilike(f"%{search}%"),
                Device.serial_number.ilike(f"%{search}%"),
                Device.brand.ilike(f"%{search}%"),
            )
        )
    return query.all()


def get_device(db: Session, device_id: int):
    device = db.query(Device).filter(Device.id == device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail="Dispositivo no encontrado")
    return device


def create_device(db: Session, device: DeviceCreate):
    existing = db.query(Device).filter(Device.serial_number == device.serial_number).first()
    if existing:
        raise HTTPException(status_code=400, detail="El numero de serie ya esta registrado")
    db_device = Device(**device.model_dump())
    db.add(db_device)
    db.commit()
    db.refresh(db_device)
    return db_device


def update_device(db: Session, device_id: int, device: DeviceUpdate):
    db_device = db.query(Device).filter(Device.id == device_id).first()
    if not db_device:
        raise HTTPException(status_code=404, detail="Dispositivo no encontrado")
    existing = db.query(Device).filter(Device.serial_number == device.serial_number, Device.id != device_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="El numero de serie ya esta registrado")
    for key, value in device.model_dump().items():
        setattr(db_device, key, value)
    db.commit()
    db.refresh(db_device)
    return db_device


def patch_device(db: Session, device_id: int, device: DevicePatch):
    db_device = db.query(Device).filter(Device.id == device_id).first()
    if not db_device:
        raise HTTPException(status_code=404, detail="Dispositivo no encontrado")
    update_data = device.model_dump(exclude_unset=True)
    if "serial_number" in update_data:
        existing = db.query(Device).filter(Device.serial_number == update_data["serial_number"], Device.id != device_id).first()
        if existing:
            raise HTTPException(status_code=400, detail="El numero de serie ya esta registrado")
    for key, value in update_data.items():
        setattr(db_device, key, value)
    db.commit()
    db.refresh(db_device)
    return db_device


def delete_device(db: Session, device_id: int):
    db_device = db.query(Device).filter(Device.id == device_id).first()
    if not db_device:
        raise HTTPException(status_code=404, detail="Dispositivo no encontrado")
    db.delete(db_device)
    db.commit()
    return {"detail": "Dispositivo eliminado correctamente"}
