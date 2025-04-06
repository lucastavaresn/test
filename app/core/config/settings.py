from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):

    current_year: int = 2025
    age_rate_increase: float = 0.005 
    value_rate_increase: float = 0.005
    coverage_percentage: float = 1.0

    model_config = SettingsConfigDict(env_file=".env")
    