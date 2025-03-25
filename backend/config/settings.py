from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import Optional


class Settings(BaseSettings):
    """Application settings."""
    # API URLs
    BASE_URL: str
    ARXIV_URL: str  # No default value - must be in .env
    
    # Application settings
    PORT: int = 8000
    ENVIRONMENT: str = "development"
    
    # Resource limits
    DOCKER_MEMORY_LIMIT: str = "2G"
    DOCKER_CPU_LIMIT: float = 1.5
    
    class Config:
        # Environment file configuration
        env_file = ".env"                    # Load variables from this file
        env_file_encoding = 'utf-8'          # Encoding of the env file
        case_sensitive = True                # ENV_VAR != env_var
        
        # Environment variable customization
        env_prefix = ''                      # Prefix for env vars (e.g., 'MY_APP_')
        env_nested_delimiter = '__'          # Delimiter for nested settings
        
        # Validation and parsing
        validate_assignment = True           # Validate values when they're set
        arbitrary_types_allowed = False      # Don't allow arbitrary types
        
        # Example JSON schema for documentation
        json_schema_extra = {
            "example": {
                "BASE_URL": "http://localhost:8000",
                "PORT": 8000,
                "ENVIRONMENT": "development"
            }
        }


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance.
    
    The Config class controls:
    1. Where to load environment variables from (.env file)
    2. How to parse them (case sensitivity, encoding)
    3. How to validate them (assignment validation)
    4. How to document them (json_schema_extra)
    """
    return Settings() 