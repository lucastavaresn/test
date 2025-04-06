# app/adapters/api/schemas.py
from pydantic import BaseModel, field_validator

from core.domain.aggregates import InsurancePolicy


class CarInputSchema(BaseModel):
    broker_fee: float
    deductible_percentage: float
    make: str
    model: str
    value: float
    year: int

class CarOutputSchema(BaseModel):
    applied_rate: float
    calculated_premium: float
    deductible_value: float
    make: str
    model: str
    policy_limit: float
    value: float
    year: int

    @classmethod
    def from_policy(cls, policy: InsurancePolicy):
        return cls(
            make=policy.car.make,
            model=policy.car.model,
            year=policy.car.year,
            value=policy.car.value.value,
            applied_rate=policy.applied_rate,
            policy_limit=policy.policy_limit,
            calculated_premium=policy.calculated_premium,
            deductible_value=policy.deductible_value,
        )
    

    @field_validator('applied_rate', 'calculated_premium', 'deductible_value', 'policy_limit', 'value')
    def format_two_decimal_places(cls, v):
        return round(v, 3)
