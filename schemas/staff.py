from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, ConfigDict


class RolEquipo(str, Enum):
    coordinador = "coordinador"
    operativo = "operativo"
    practicante = "practicante"


class RegistroPersonal(BaseModel):
    nombre_completo: str = Field(..., min_length=2, max_length=150, examples=["Ana Torres"])
    correo: EmailStr
    rol: RolEquipo
    notas: Optional[str] = Field(None, max_length=500)


class ActualizacionCompleta(BaseModel):
    nombre_completo: str = Field(..., min_length=2, max_length=150)
    correo: EmailStr
    rol: RolEquipo
    activo: bool = True
    notas: Optional[str] = None


class ParchePersonal(BaseModel):
    nombre_completo: Optional[str] = Field(None, min_length=2, max_length=150)
    correo: Optional[EmailStr] = None
    rol: Optional[RolEquipo] = None
    activo: Optional[bool] = None
    notas: Optional[str] = None


class FichaPersonal(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    uid: int
    nombre_completo: str
    correo: str
    rol: str
    activo: bool
    fecha_alta: datetime
    notas: Optional[str] = None
