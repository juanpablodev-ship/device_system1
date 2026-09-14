from typing import List

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from core.database import get_session
from schemas.staff import RegistroPersonal, ActualizacionCompleta, ParchePersonal, FichaPersonal, RolEquipo
from crud.staff import GestorPersonal

router = APIRouter(prefix="/personal", tags=["Personal"])


def _gestor(db: Session = Depends(get_session)) -> GestorPersonal:
    return GestorPersonal(db)


@router.get("", response_model=List[FichaPersonal], summary="Consultar plantilla completa")
def obtener_plantilla(
    rol: RolEquipo | None = Query(None, description="Filtrar por rol asignado"),
    solo_activos: bool | None = Query(None, alias="activo", description="Solo personal activo"),
    ordenar_por: str = Query("nombre_completo", pattern="^(nombre_completo|fecha_alta)$"),
    gestor: GestorPersonal = Depends(_gestor),
):
    return gestor.listar_todos(rol=rol, solo_activos=solo_activos, ordenar_por=ordenar_por)


@router.get("/{uid}", response_model=FichaPersonal, summary="Buscar personal por identificador")
def obtener_por_id(uid: int, gestor: GestorPersonal = Depends(_gestor)):
    return gestor.buscar_por_id(uid)


@router.post("", response_model=FichaPersonal, status_code=201, summary="Dar de alta nuevo personal")
def registrar_personal(datos: RegistroPersonal, gestor: GestorPersonal = Depends(_gestor)):
    return gestor.alta(datos)


@router.put("/{uid}", response_model=FichaPersonal, summary="Reemplazo total de registro")
def reemplazar_personal(uid: int, datos: ActualizacionCompleta, gestor: GestorPersonal = Depends(_gestor)):
    return gestor.reemplazo(uid, datos)


@router.patch("/{uid}", response_model=FichaPersonal, summary="Ajuste selectivo de campos")
def ajustar_personal(uid: int, datos: ParchePersonal, gestor: GestorPersonal = Depends(_gestor)):
    return gestor.ajuste_parcial(uid, datos)


@router.delete("/{uid}", status_code=204, summary="Dar de baja personal")
def eliminar_personal(uid: int, gestor: GestorPersonal = Depends(_gestor)):
    gestor.baja(uid)
