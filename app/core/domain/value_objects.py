from dataclasses import dataclass

@dataclass()
class Address:
    city: str
    state: str
    street: str
    zip_code: str

@dataclass()
class Money:
    value: float

@dataclass()
class Rate:
    value: float