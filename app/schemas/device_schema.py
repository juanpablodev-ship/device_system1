from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class DeviceCreate(BaseModel):
    name: str = Field(..., min_length=1, description="Nombre del dispositivo")
    serial_number: str = Field(..., min_length=1, description="Numero de serie unico")
    device_type: str = Field(..., description="Tipo de dispositivo")
    brand: Optional[str] = Field(None, description="Marca del dispositivo")
    is_available: bool = Field(default=True, description="Disponibilidad del dispositivo")


class DeviceUpdate(BaseModel):
    name: str = Field(..., min_length=1, description="Nombre del dispositivo")
    serial_number: str = Field(..., min_length=1, description="Numero de serie unico")
    device_type: str = Field(..., description="Tipo de dispositivo")
    brand: Optional[str] = Field(None, description="Marca del dispositivo")
    is_available: bool = Field(default=True, description="Disponibilidad del dispositivo")


class DevicePatch(BaseModel):
    name: Optional[str] = Field(None, min_length=1, description="Nombre del dispositivo")
    serial_number: Optional[str] = Field(None, min_length=1, description="Numero de serie unico")
    device_type: Optional[str] = Field(None, description="Tipo de dispositivo")
    brand: Optional[str] = Field(None, description="Marca del dispositivo")
    is_available: Optional[bool] = Field(None, description="Disponibilidad del dispositivo")


class DeviceResponse(BaseModel):
    id: int
    name: str
    serial_number: str
    device_type: str
    brand: Optional[str] = None
    is_available: bool
    created_at: datetime

    model_config = {"from_attributes": True}
