from fastapi import APIRouter

from api.v1.staff import router as staff_router

api_router = APIRouter()
api_router.include_router(staff_router)
