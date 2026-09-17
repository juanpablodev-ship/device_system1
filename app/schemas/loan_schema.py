from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class LoanCreate(BaseModel):
    user_id: int = Field(..., description="ID del usuario")
    device_id: int = Field(..., description="ID del dispositivo")


class LoanResponse(BaseModel):
    id: int
    user_id: int
    device_id: int
    loan_date: datetime
    return_date: Optional[datetime] = None
    status: str

    model_config = {"from_attributes": True}


class UserInfo(BaseModel):
    id: int
    name: str
    email: str

    model_config = {"from_attributes": True}


class DeviceInfo(BaseModel):
    id: int
    name: str
    serial_number: str
    device_type: str

    model_config = {"from_attributes": True}


class LoanDetailResponse(BaseModel):
    id: int
    loan_date: datetime
    return_date: Optional[datetime] = None
    status: str
    user: UserInfo
    device: DeviceInfo

    model_config = {"from_attributes": True}
