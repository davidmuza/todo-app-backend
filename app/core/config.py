from dataclasses import dataclass

@dataclass
class Settings:
    DATABASE_URL: str = "postgresql+asyncpg://muzati:muzati777@localhost:5432/database"
    
def get_settings() -> Settings:
    return Settings