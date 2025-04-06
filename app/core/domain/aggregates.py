from dataclasses import dataclass
from core.domain.entities import Car

@dataclass
class InsurancePolicy:
    car: Car
    applied_rate: float
    policy_limit: float  
    calculated_premium: float 
    deductible_value: float 