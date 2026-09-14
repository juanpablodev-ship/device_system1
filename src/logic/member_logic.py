from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.entities.member_entity import Member
from src.dto.member_dto import MemberRegister, MemberFullUpdate, MemberPartialUpdate


def _verify_unique_email(db: Session, email: str, skip_id: int = None) -> None:
    query = db.query(Member).filter(Member.contact_email == email)
    if skip_id is not None:
        query = query.filter(Member.id != skip_id)
    if query.first() is not None:
        raise HTTPException(status_code=400, detail="El correo ya está registrado")


def fetch_members(db: Session, position=None, is_available=None, sort_by="full_name") -> list:
    """Obtiene todos los miembros aplicando filtros y orden."""
    stmt = db.query(Member)
    if position is not None:
        stmt = stmt.filter(Member.position == position.value if hasattr(position, "value") else position)
    if is_available is not None:
        stmt = stmt.filter(Member.is_available == is_available)
    if sort_by == "joined_on":
        stmt = stmt.order_by(Member.joined_on.desc())
    else:
        stmt = stmt.order_by(Member.full_name.asc())
    return stmt.all()


def fetch_member_by_id(db: Session, member_id: int) -> Member | None:
    return db.query(Member).filter(Member.id == member_id).first()


def register_member(db: Session, payload: MemberRegister) -> Member:
    """Registra un nuevo miembro. Lanza 400 si el correo ya existe."""
    _verify_unique_email(db, payload.contact_email)
    record = Member(**payload.model_dump())
    db.add(record)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="El correo ya está registrado")
    db.refresh(record)
    return record


def full_update_member(db: Session, member_id: int, payload: MemberFullUpdate) -> Member:
    """Actualización completa (PUT). Lanza 404 o 400 según el caso."""
    record = fetch_member_by_id(db, member_id)
    if record is None:
        raise HTTPException(status_code=404, detail="Miembro no encontrado")
    _verify_unique_email(db, payload.contact_email, skip_id=member_id)
    for attr, val in payload.model_dump().items():
        setattr(record, attr, val)
    db.commit()
    db.refresh(record)
    return record


def partial_update_member(db: Session, member_id: int, payload: MemberPartialUpdate) -> Member:
    """Actualización parcial (PATCH). Lanza 400 si el body está vacío."""
    changes = payload.model_dump(exclude_unset=True)
    if not changes:
        raise HTTPException(status_code=400, detail="No se enviaron campos para actualizar")
    if "contact_email" in changes:
        _verify_unique_email(db, changes["contact_email"], skip_id=member_id)
    record = fetch_member_by_id(db, member_id)
    if record is None:
        raise HTTPException(status_code=404, detail="Miembro no encontrado")
    for attr, val in changes.items():
        setattr(record, attr, val)
    db.commit()
    db.refresh(record)
    return record


def remove_member(db: Session, member_id: int) -> None:
    """Elimina un miembro por ID. Lanza 404 si no existe."""
    record = fetch_member_by_id(db, member_id)
    if record is None:
        raise HTTPException(status_code=404, detail="Miembro no encontrado")
    db.delete(record)
    db.commit()
