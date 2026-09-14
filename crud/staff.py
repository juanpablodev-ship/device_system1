from sqlalchemy.orm import Session

from models.staff import Staff
from schemas.staff import RegistroPersonal, ActualizacionCompleta, ParchePersonal
from core.exceptions import DuplicateRecord, RecordNotFound, EmptyPayload


class GestorPersonal:
    def __init__(self, db: Session):
        self.db = db

    def _correo_existe(self, correo: str, excluid: int | None = None) -> bool:
        q = self.db.query(Staff).filter(Staff.correo == correo)
        if excluid is not None:
            q = q.filter(Staff.uid != excluid)
        return q.first() is not None

    def _buscar_por_uid(self, uid: int) -> Staff:
        registro = self.db.query(Staff).filter(Staff.uid == uid).first()
        if registro is None:
            raise RecordNotFound("Personal", uid)
        return registro

    def listar_todos(self, rol: str | None = None, solo_activos: bool | None = None, ordenar_por: str = "nombre_completo") -> list[Staff]:
        consulta = self.db.query(Staff)
        if rol is not None:
            consulta = consulta.filter(Staff.rol == rol)
        if solo_activos is not None:
            consulta = consulta.filter(Staff.activo == solo_activos)
        if ordenar_por == "fecha_alta":
            consulta = consulta.order_by(Staff.fecha_alta.desc())
        else:
            consulta = consulta.order_by(Staff.nombre_completo.asc())
        return consulta.all()

    def buscar_por_id(self, uid: int) -> Staff:
        return self._buscar_por_uid(uid)

    def alta(self, datos: RegistroPersonal) -> Staff:
        if self._correo_existe(datos.correo):
            raise DuplicateRecord("correo")
        nuevo = Staff(**datos.model_dump())
        self.db.add(nuevo)
        self.db.commit()
        self.db.refresh(nuevo)
        return nuevo

    def reemplazo(self, uid: int, datos: ActualizacionCompleta) -> Staff:
        registro = self._buscar_por_uid(uid)
        if self._correo_existe(datos.correo, excluid=uid):
            raise DuplicateRecord("correo")
        for campo, valor in datos.model_dump().items():
            setattr(registro, campo, valor)
        self.db.commit()
        self.db.refresh(registro)
        return registro

    def ajuste_parcial(self, uid: int, datos: ParchePersonal) -> Staff:
        cambios = datos.model_dump(exclude_unset=True)
        if not cambios:
            raise EmptyPayload()
        if "correo" in cambios and self._correo_existe(cambios["correo"], excluid=uid):
            raise DuplicateRecord("correo")
        registro = self._buscar_por_uid(uid)
        for campo, valor in cambios.items():
            setattr(registro, campo, valor)
        self.db.commit()
        self.db.refresh(registro)
        return registro

    def baja(self, uid: int) -> None:
        registro = self._buscar_por_uid(uid)
        self.db.delete(registro)
        self.db.commit()
