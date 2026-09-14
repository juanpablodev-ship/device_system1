from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String

from core.database import Base


class Staff(Base):
    __tablename__ = "staff"

    uid = Column(Integer, primary_key=True, autoincrement=True)
    nombre_completo = Column(String(150), nullable=False)
    correo = Column(String(300), unique=True, nullable=False, index=True)
    rol = Column(String(30), nullable=False)
    activo = Column(Boolean, default=True, nullable=False)
    fecha_alta = Column(DateTime, default=datetime.utcnow, nullable=False)
    notas = Column(String(500), nullable=True)
