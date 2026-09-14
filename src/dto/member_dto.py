from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class MemberRole(str, Enum):
    manager = "manager"
    staff = "staff"
    intern = "intern"


class MemberBase(BaseModel):
    full_name: str = Field(..., min_length=3, description="Nombre completo del miembro")
    contact_email: EmailStr
    position: MemberRole
    is_available: bool = True


class MemberRegister(MemberBase):
    pass


class MemberFullUpdate(MemberBase):
    pass


class MemberPartialUpdate(BaseModel):
    full_name: Optional[str] = Field(None, min_length=3, description="Nombre completo del miembro")
    contact_email: Optional[EmailStr] = None
    position: Optional[MemberRole] = None
    is_available: Optional[bool] = None


class MemberOut(MemberBase):
    id: int
    joined_on: datetime

    model_config = {"from_attributes": True}
