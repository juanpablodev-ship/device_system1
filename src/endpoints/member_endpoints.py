from fastapi import APIRouter, Query, Path, Depends, HTTPException
from typing import List, Optional
from sqlalchemy.orm import Session

from src.dto.member_dto import (
    MemberRegister, MemberFullUpdate, MemberPartialUpdate, MemberOut, MemberRole
)
from src.injectors.header_injector import inject_response_headers
from src.injectors.session_injector import obtain_session
import src.logic.member_logic as logic

router = APIRouter(prefix="/members", tags=["Members"])


@router.get(
    "",
    response_model=List[MemberOut],
    summary="Listar miembros",
    description="Retorna todos los miembros registrados. "
                "Permite filtrar por **posición** y/o **disponibilidad**.",
    response_description="Lista de miembros que cumplen con los filtros.",
)
def list_all_members(
    position: Optional[MemberRole] = Query(None, description="Filtrar por posición: manager, staff o intern"),
    is_available: Optional[bool] = Query(None, description="Filtrar por disponibilidad: true o false"),
    sort_by: str = Query("full_name", pattern="^(full_name|joined_on)$", description="Ordenar por nombre o fecha de ingreso"),
    db: Session = Depends(obtain_session),
    _: None = Depends(inject_response_headers),
):
    return logic.fetch_members(db, position=position, is_available=is_available, sort_by=sort_by)


@router.get(
    "/{member_id}",
    response_model=MemberOut,
    summary="Consultar miembro por ID",
    description="Retorna un único miembro por su **ID**. "
                "Responde con **404** si no existe.",
    response_description="Datos completos del miembro encontrado.",
)
def find_member(
    member_id: int = Path(..., description="ID del miembro"),
    db: Session = Depends(obtain_session),
    _: None = Depends(inject_response_headers),
):
    result = logic.fetch_member_by_id(db, member_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Miembro no encontrado")
    return result


@router.post(
    "",
    response_model=MemberOut,
    status_code=201,
    summary="Registrar miembro",
    description="Alta de un nuevo miembro. El correo debe ser único. "
                "Responde con **201 Created**.",
    response_description="Datos del miembro registrado, incluyendo su ID.",
)
def create_new_member(
    payload: MemberRegister,
    db: Session = Depends(obtain_session),
    _: None = Depends(inject_response_headers),
):
    return logic.register_member(db, payload)


@router.put(
    "/{member_id}",
    response_model=MemberOut,
    summary="Actualizar miembro (completo)",
    description="Reemplaza toda la información de un miembro. "
                "Se requieren todos los campos. "
                "Responde con **200 OK**, **404** o **400**.",
    response_description="Datos actualizados del miembro.",
)
def replace_member(
    payload: MemberFullUpdate,
    member_id: int = Path(..., description="ID del miembro a actualizar"),
    db: Session = Depends(obtain_session),
    _: None = Depends(inject_response_headers),
):
    return logic.full_update_member(db, member_id, payload)


@router.patch(
    "/{member_id}",
    response_model=MemberOut,
    summary="Actualizar miembro (parcial)",
    description="Modifica solo los campos enviados. "
                "Si no se envía ningún campo → **400 Bad Request**. "
                "Responde con **200 OK**, **404** o **400**.",
    response_description="Datos del miembro con campos actualizados.",
)
def modify_member_fields(
    payload: MemberPartialUpdate,
    member_id: int = Path(..., description="ID del miembro a modificar"),
    db: Session = Depends(obtain_session),
    _: None = Depends(inject_response_headers),
):
    return logic.partial_update_member(db, member_id, payload)


@router.delete(
    "/{member_id}",
    status_code=204,
    summary="Eliminar miembro",
    description="Borra un miembro del sistema de forma permanente. "
                "Responde con **204 No Content** o **404**.",
    response_description="Sin contenido. Operación exitosa.",
)
def delete_existing_member(
    member_id: int = Path(..., description="ID del miembro a eliminar"),
    db: Session = Depends(obtain_session),
    _: None = Depends(inject_response_headers),
):
    logic.remove_member(db, member_id)
