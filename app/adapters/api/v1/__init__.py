from fastapi import APIRouter
from .car_insurance_route import router as car_insurance_router

router = APIRouter()
router.include_router(car_insurance_router, tags=["Car Insurance"])