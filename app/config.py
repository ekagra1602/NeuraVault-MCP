https://github.com/ekagra1602/NeuraVault-MCPfrom functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = "NeuraVault MCP Server"
    debug: bool = True
    host: str = "0.0.0.0"
    port: int = 8000

    class Config:
        env_file = ".env"


@lru_cache
def get_settings() -> Settings:
    """Return a cached instance of the application settings."""
    return Settings() 