from fastapi import APIRouter
from adapters.api.schemas import CarInputSchema, CarOutputSchema
from core.config.settings import Settings
from core.domain.entities import Car
from core.domain.services.premium_calculator import PremiumCalculator
from core.domain.value_objects import Money

router = APIRouter()

settings = Settings()
calculator = PremiumCalculator(settings)

@router.post("/calculate_premium", response_model=CarOutputSchema)
def calculate_premium(car_input: CarInputSchema):

    car = Car(
        make=car_input.make,
        model=car_input.model,
        year=car_input.year,
        value=Money(value=car_input.value),
        deductible_percentage=car_input.deductible_percentage,
        broker_fee=Money(value=car_input.broker_fee)
    )

    policy = calculator.calculate_premium(car)
    return CarOutputSchema.from_policy(policy)
