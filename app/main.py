from fastapi import FastAPI
from app.routes.user_routes import router as user_router
from app.routes.device_routes import router as device_router
from app.routes.loan_routes import router as loan_router
from app.database.connection import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="device_systems", version="2.0", description="API REST para la gestion de usuarios, dispositivos y prestamos del sistema device_systems.")

app.include_router(user_router)
app.include_router(device_router)
app.include_router(loan_router)


@app.get("/", tags=["root"])
def read_root():
    return {"mensaje": "Bienvenido a device_systems v2.0"}
