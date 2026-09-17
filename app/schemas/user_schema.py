from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from enum import Enum


class Role(str, Enum):
    admin = "admin"
    support = "support"
    user = "user"


class UserCreate(BaseModel):
    name: str = Field(..., min_length=3, description="Nombre del usuario")
    email: EmailStr = Field(..., description="Correo electronico")
    role: Role = Field(..., description="Rol del usuario")
    is_active: bool = Field(default=True, description="Estado activo/inactivo")


class UserUpdate(BaseModel):
    name: str = Field(..., min_length=3, description="Nombre del usuario")
    email: EmailStr = Field(..., description="Correo electronico")
    role: Role = Field(..., description="Rol del usuario")
    is_active: bool = Field(default=True, description="Estado activo/inactivo")


class UserPatch(BaseModel):
    name: Optional[str] = Field(None, min_length=3, description="Nombre del usuario")
    email: Optional[EmailStr] = Field(None, description="Correo electronico")
    role: Optional[Role] = Field(None, description="Rol del usuario")
    is_active: Optional[bool] = Field(None, description="Estado activo/inactivo")


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    role: Role
    is_active: bool

    model_config = {"from_attributes": True}
