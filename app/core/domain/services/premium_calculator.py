from core.domain.entities import Car
from core.domain.aggregates import InsurancePolicy
from core.domain.value_objects import Money, Rate
from core.config.settings import Settings

class PremiumCalculator:
    def __init__(self, settings: Settings):
        self.settings = settings

    def _calculate_base_policy_limit(self, car_value: Money) -> Money:
        return Money(value=car_value.value * self.settings.coverage_percentage)

    def _calculate_base_premium(self, car_value: Money, applied_rate: Rate) -> Money:
        return Money(value=car_value.value * applied_rate.value)

    def _calculate_deductible_discount(self, base_premium: Money, deductible_percentage: float) -> Money:
        return Money(value=base_premium.value * deductible_percentage)

    def _calculate_deductible_value(self, base_policy_limit: Money, deductible_percentage: float) -> Money:
        return Money(value=base_policy_limit.value * deductible_percentage)

    def _calculate_final_policy_limit(self, base_policy_limit: Money, deductible_value: Money) -> Money:
        return Money(value=base_policy_limit.value - deductible_value.value)

    def _calculate_final_premium(self, base_premium: Money, deductible_discount: Money, broker_fee: Money) -> Money:
        broker_fee_value = base_premium.value * broker_fee.value / 100
        final_premium = (base_premium.value - deductible_discount.value) + broker_fee_value
        return Money(value=final_premium)

    def _calculate_rate_by_age(self, car_year: int) -> float:
        return (self.settings.current_year - car_year) * self.settings.age_rate_increase

    def _calculate_rate_by_value(self, car_value: Money) -> float:
        return (car_value.value // 10000) * self.settings.value_rate_increase

    def calculate_premium(self, car: Car) -> InsurancePolicy:
        applied_rate = self.calculate_rate(car)
        base_premium = self._calculate_base_premium(car.value, applied_rate)
        deductible_discount = self._calculate_deductible_discount(base_premium, car.deductible_percentage)
        final_premium = self._calculate_final_premium(base_premium, deductible_discount, car.broker_fee)

        base_policy_limit = self._calculate_base_policy_limit(car.value)
        deductible_value = self._calculate_deductible_value(base_policy_limit, car.deductible_percentage)
        final_policy_limit = self._calculate_final_policy_limit(base_policy_limit, deductible_value)

        return InsurancePolicy(
            car=car,
            applied_rate=applied_rate.value,
            policy_limit=final_policy_limit.value,
            calculated_premium=final_premium.value,
            deductible_value=deductible_value.value,
        )

    def calculate_rate(self, car: Car) -> Rate:
        age_rate = self._calculate_rate_by_age(car.year)
        value_rate = self._calculate_rate_by_value(car.value)
        total_rate = age_rate + value_rate
        return Rate(value=total_rate)
