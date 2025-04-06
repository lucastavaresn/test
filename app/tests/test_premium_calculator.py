import pytest
from core.config.settings import Settings
from core.domain.entities import Car
from core.domain.services.premium_calculator import PremiumCalculator
from core.domain.value_objects import Money, Rate


@pytest.fixture
def default_settings():
    return Settings(
        current_year=2025,
        age_rate_increase=0.005,
        value_rate_increase=0.005,
        coverage_percentage=1.0
    )

@pytest.fixture
def premium_calculator(default_settings):
    return PremiumCalculator(default_settings)

@pytest.fixture
def sample_car():
    return Car(
        make="Ford",
        model="Ka SE 1.0",
        year=2018,
        value=Money(value=42000.00),
        deductible_percentage=0.10,
        broker_fee=Money(value=50.0)
    )

def test_calculate_base_policy_limit(premium_calculator, sample_car, default_settings):
    base_policy_limit = premium_calculator._calculate_base_policy_limit(sample_car.value)
    expected_limit = sample_car.value.value * default_settings.coverage_percentage
    assert base_policy_limit.value == pytest.approx(expected_limit)

def test_calculate_base_policy_limit_zero_value(premium_calculator, default_settings):
    car_value = Money(value=0.0)
    base_policy_limit = premium_calculator._calculate_base_policy_limit(car_value)
    assert base_policy_limit.value == pytest.approx(0.0)

def test_calculate_base_premium(premium_calculator, sample_car):
    applied_rate = Rate(value=0.055)
    base_premium = premium_calculator._calculate_base_premium(sample_car.value, applied_rate)
    expected_premium = sample_car.value.value * applied_rate.value
    assert base_premium.value == pytest.approx(expected_premium)

def test_calculate_base_premium_zero_value(premium_calculator):
    car_value = Money(value=0.0)
    applied_rate = Rate(value=0.055)
    base_premium = premium_calculator._calculate_base_premium(car_value, applied_rate)
    assert base_premium.value == pytest.approx(0.0)

def test_calculate_deductible_discount(premium_calculator):
    base_premium = Money(value=2310.00)
    deductible_percentage = 0.10
    discount = premium_calculator._calculate_deductible_discount(base_premium, deductible_percentage)
    expected_discount = base_premium.value * deductible_percentage
    assert discount.value == pytest.approx(expected_discount)

def test_calculate_deductible_discount_zero_premium(premium_calculator):
    base_premium = Money(value=0.0)
    deductible_percentage = 0.10
    discount = premium_calculator._calculate_deductible_discount(base_premium, deductible_percentage)
    assert discount.value == pytest.approx(0.0)

def test_calculate_deductible_value(premium_calculator):
    base_policy_limit = Money(value=42000.00)
    deductible_percentage = 0.10
    deductible = premium_calculator._calculate_deductible_value(base_policy_limit, deductible_percentage)
    expected_deductible = base_policy_limit.value * deductible_percentage
    assert deductible.value == pytest.approx(expected_deductible)

def test_calculate_deductible_value_zero_limit(premium_calculator):
    base_policy_limit = Money(value=0.0)
    deductible_percentage = 0.10
    deductible = premium_calculator._calculate_deductible_value(base_policy_limit, deductible_percentage)
    assert deductible.value == pytest.approx(0.0)

def test_calculate_final_policy_limit(premium_calculator):
    base_policy_limit = Money(value=42000.00)
    deductible_value = Money(value=4200.00)
    final_limit = premium_calculator._calculate_final_policy_limit(base_policy_limit, deductible_value)
    expected_limit = base_policy_limit.value - deductible_value.value
    assert final_limit.value == pytest.approx(expected_limit)

def test_calculate_final_policy_limit_deductible_equals_limit(premium_calculator):
    base_policy_limit = Money(value=42000.00)
    deductible_value = Money(value=42000.00)
    final_limit = premium_calculator._calculate_final_policy_limit(base_policy_limit, deductible_value)
    assert final_limit.value == pytest.approx(0.0)

def test_calculate_final_premium(premium_calculator):
    base_premium = Money(value=2310.00)
    deductible_discount = Money(value=231.00)
    broker_fee = Money(value=50.0)
    final_premium = premium_calculator._calculate_final_premium(base_premium, deductible_discount, broker_fee)
    expected_premium = (base_premium.value - deductible_discount.value) + (base_premium.value * broker_fee.value / 100)
    assert final_premium.value == pytest.approx(expected_premium)

def test_calculate_final_premium_zero_base_premium(premium_calculator):
    base_premium = Money(value=0.0)
    deductible_discount = Money(value=0.0)
    broker_fee = Money(value=50.0)
    final_premium = premium_calculator._calculate_final_premium(base_premium, deductible_discount, broker_fee)
    assert final_premium.value == pytest.approx(0.0)

def test_calculate_rate_by_age(premium_calculator, default_settings):
    car_year = 2018
    age_rate = premium_calculator._calculate_rate_by_age(car_year)
    expected_rate = (default_settings.current_year - car_year) * default_settings.age_rate_increase
    assert age_rate == pytest.approx(expected_rate)

def test_calculate_rate_by_age_same_year(premium_calculator, default_settings):
    car_year = default_settings.current_year
    age_rate = premium_calculator._calculate_rate_by_age(car_year)
    assert age_rate == pytest.approx(0.0)


def test_calculate_rate_by_value(premium_calculator):
    car_value = Money(value=42000.00)
    value_rate = premium_calculator._calculate_rate_by_value(car_value)
    expected_rate = (car_value.value // 10000) * premium_calculator.settings.value_rate_increase
    assert value_rate == pytest.approx(expected_rate)

def test_calculate_rate_by_value_low_value(premium_calculator):
    car_value = Money(value=5000.00)
    value_rate = premium_calculator._calculate_rate_by_value(car_value)
    assert value_rate == pytest.approx(0.0)

def test_calculate_rate(premium_calculator, sample_car):
    rate = premium_calculator.calculate_rate(sample_car)
    expected_age_rate = (premium_calculator.settings.current_year - sample_car.year) * premium_calculator.settings.age_rate_increase
    expected_value_rate = (sample_car.value.value // 10000) * premium_calculator.settings.value_rate_increase
    expected_total_rate = expected_age_rate + expected_value_rate
    assert rate.value == pytest.approx(expected_total_rate)

def test_calculate_rate_zero_age_and_value_rate(premium_calculator):
    car = Car(
        make="Test",
        model="Test",
        year=premium_calculator.settings.current_year,
        value=Money(value=5000.00),
        deductible_percentage=0.10,
        broker_fee=Money(value=10.0)
    )
    rate = premium_calculator.calculate_rate(car)
    assert rate.value == pytest.approx(0.0)


def test_calculate_premium_integration(premium_calculator, sample_car):
    policy = premium_calculator.calculate_premium(sample_car)
    expected_applied_rate = (premium_calculator.settings.current_year - sample_car.year) * premium_calculator.settings.age_rate_increase + \
                            (sample_car.value.value // 10000) * premium_calculator.settings.value_rate_increase
    expected_base_premium = sample_car.value.value * expected_applied_rate
    expected_deductible_discount = expected_base_premium * sample_car.deductible_percentage
    expected_broker_fee_value = expected_base_premium * sample_car.broker_fee.value / 100
    expected_final_premium = (expected_base_premium - expected_deductible_discount) + expected_broker_fee_value
    expected_base_policy_limit = sample_car.value.value * premium_calculator.settings.coverage_percentage
    expected_deductible_value = expected_base_policy_limit * sample_car.deductible_percentage
    expected_final_policy_limit = expected_base_policy_limit - expected_deductible_value

    assert policy.applied_rate == pytest.approx(expected_applied_rate)
    assert policy.calculated_premium == pytest.approx(expected_final_premium)
    assert policy.deductible_value == pytest.approx(expected_deductible_value)
    assert policy.policy_limit == pytest.approx(expected_final_policy_limit)

def test_calculate_premium_zero_car_value_integration(premium_calculator, default_settings):
    zero_value_car = Car(
        make="Test",
        model="Test",
        year=2020,
        value=Money(value=0.0),
        deductible_percentage=0.10,
        broker_fee=Money(value=10.0)
    )
    policy = premium_calculator.calculate_premium(zero_value_car)
    assert policy.applied_rate == pytest.approx((default_settings.current_year - zero_value_car.year) * default_settings.age_rate_increase)
    assert policy.calculated_premium == pytest.approx(0.0)
    assert policy.deductible_value == pytest.approx(0.0)
    assert policy.policy_limit == pytest.approx(0.0)