from dataclasses import dataclass
from core.domain.value_objects import Money

@dataclass
class Car:
    broker_fee: Money
    deductible_percentage: float
    make: str
    model: str
    value: Money
    year: int