from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String

from src.persistence.engine import Base


class Member(Base):
    __tablename__ = "members"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(120), nullable=False)
    contact_email = Column(String(255), unique=True, nullable=False, index=True)
    position = Column(String(20), nullable=False)
    is_available = Column(Boolean, nullable=False, default=True)
    joined_on = Column(DateTime, nullable=False, default=datetime.utcnow)
