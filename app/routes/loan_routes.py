from fastapi import APIRouter, Depends, Response
from typing import Optional
from sqlalchemy.orm import Session

from app.dependencies.database_dependency import get_db
from app.schemas.loan_schema import LoanCreate, LoanResponse, LoanDetailResponse
from app.services import loan_service

router = APIRouter(prefix="/loans", tags=["loans"])


@router.get("/", response_model=list[LoanDetailResponse], summary="Listar prestamos", description="Obtiene la lista de todos los prestamos con informacion de usuario y dispositivo. Filtros opcionales por estado, usuario, dispositivo, email de usuario y tipo de dispositivo.")
def get_loans(
    response: Response,
    status: Optional[str] = None,
    user_id: Optional[int] = None,
    device_id: Optional[int] = None,
    user_email: Optional[str] = None,
    device_type: Optional[str] = None,
    db: Session = Depends(get_db),
):
    response.headers["X-App-Name"] = "device_systems"
    response.headers["X-API-Version"] = "2.0"
    return loan_service.get_loans(db, status=status, user_id=user_id, device_id=device_id, user_email=user_email, device_type=device_type)


@router.get("/details", response_model=list[LoanDetailResponse], summary="Detalle de prestamos", description="Obtiene todos los prestamos con informacion detallada de usuario y dispositivo.")
def get_loan_details(response: Response, db: Session = Depends(get_db)):
    response.headers["X-App-Name"] = "device_systems"
    response.headers["X-API-Version"] = "2.0"
    return loan_service.get_loans(db)


@router.get("/{loan_id}", response_model=LoanDetailResponse, summary="Obtener prestamo por ID", description="Obtiene los datos de un prestamo especifico con informacion de usuario y dispositivo.")
def get_loan(loan_id: int, response: Response, db: Session = Depends(get_db)):
    response.headers["X-App-Name"] = "device_systems"
    response.headers["X-API-Version"] = "2.0"
    return loan_service.get_loan(db, loan_id)


@router.post("/", response_model=LoanResponse, status_code=201, summary="Crear prestamo", description="Registra un nuevo prestamo. Valida que el usuario y dispositivo existan, y que el dispositivo este disponible.")
def create_loan(loan: LoanCreate, response: Response, db: Session = Depends(get_db)):
    response.headers["X-App-Name"] = "device_systems"
    response.headers["X-API-Version"] = "2.0"
    return loan_service.create_loan(db, loan)


@router.patch("/{loan_id}/return", response_model=LoanResponse, summary="Devolver dispositivo", description="Marca un prestamo como devuelto y libera el dispositivo.")
def return_loan(loan_id: int, response: Response, db: Session = Depends(get_db)):
    response.headers["X-App-Name"] = "device_systems"
    response.headers["X-API-Version"] = "2.0"
    return loan_service.return_loan(db, loan_id)


@router.get("/user/{user_id}", response_model=list[LoanDetailResponse], summary="Prestamos de un usuario", description="Obtiene todos los prestamos de un usuario especifico.")
def get_user_loans(user_id: int, response: Response, db: Session = Depends(get_db)):
    response.headers["X-App-Name"] = "device_systems"
    response.headers["X-API-Version"] = "2.0"
    return loan_service.get_user_loans(db, user_id)


@router.get("/device/{device_id}", response_model=list[LoanDetailResponse], summary="Prestamos de un dispositivo", description="Obtiene el historial de prestamos de un dispositivo especifico.")
def get_device_loans(device_id: int, response: Response, db: Session = Depends(get_db)):
    response.headers["X-App-Name"] = "device_systems"
    response.headers["X-API-Version"] = "2.0"
    return loan_service.get_device_loans(db, device_id)
