from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


DB_PATH = "sqlite:///./talent_hub.db"

engine = create_engine(
    DB_PATH,
    connect_args={"check_same_thread": False},
)
SessionFactory = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def obtain_session():
    session = SessionFactory()
    try:
        yield session
    finally:
        session.close()
