from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime, timezone

from app.models.loan_model import Loan
from app.models.user_model import User
from app.models.device_model import Device
from app.schemas.loan_schema import LoanCreate


def get_loans(db: Session, status: str = None, user_id: int = None, device_id: int = None, user_email: str = None, device_type: str = None):
    query = db.query(Loan)
    if status:
        query = query.filter(Loan.status == status)
    if user_id:
        query = query.filter(Loan.user_id == user_id)
    if device_id:
        query = query.filter(Loan.device_id == device_id)
    if user_email:
        query = query.join(User).filter(User.email.ilike(f"%{user_email}%"))
    if device_type:
        query = query.join(Device).filter(Device.device_type.ilike(f"%{device_type}%"))
    return query.all()


def get_loan(db: Session, loan_id: int):
    loan = db.query(Loan).filter(Loan.id == loan_id).first()
    if not loan:
        raise HTTPException(status_code=404, detail="Prestamo no encontrado")
    return loan


def create_loan(db: Session, loan: LoanCreate):
    user = db.query(User).filter(User.id == loan.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    device = db.query(Device).filter(Device.id == loan.device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail="Dispositivo no encontrado")
    if not device.is_available:
        raise HTTPException(status_code=409, detail="El dispositivo no esta disponible")

    db_loan = Loan(user_id=loan.user_id, device_id=loan.device_id, status="active")
    db.add(db_loan)
    device.is_available = False
    db.commit()
    db.refresh(db_loan)
    return db_loan


def return_loan(db: Session, loan_id: int):
    loan = db.query(Loan).filter(Loan.id == loan_id).first()
    if not loan:
        raise HTTPException(status_code=404, detail="Prestamo no encontrado")
    if loan.status == "returned":
        raise HTTPException(status_code=409, detail="El prestamo ya fue devuelto")

    loan.status = "returned"
    loan.return_date = datetime.now(timezone.utc)
    device = db.query(Device).filter(Device.id == loan.device_id).first()
    if device:
        device.is_available = True
    db.commit()
    db.refresh(loan)
    return loan


def get_user_loans(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return db.query(Loan).filter(Loan.user_id == user_id).all()


def get_device_loans(db: Session, device_id: int):
    device = db.query(Device).filter(Device.id == device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail="Dispositivo no encontrado")
    return db.query(Loan).filter(Loan.device_id == device_id).all()
