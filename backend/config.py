"""
Central place for all environment-driven configuration.

Everything here is read once at startup from environment variables (or a .env file in local
development). Import `settings` anywhere you need a config value instead of calling
os.environ directly — that keeps all configuration discoverable in one place.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # Database
    database_url: str = "postgresql://controlplane:controlplane@localhost:5432/controlplane"

    # LLM providers — set whichever one(s) you actually have keys for.
    # Groq and Gemini both have free tiers; Ollama needs no key at all (see llm_router.py).
    openai_api_key: str = ""
    anthropic_api_key: str = ""
    groq_api_key: str = ""
    gemini_api_key: str = ""

    # Model names use LiteLLM's "<provider>/<model>" format. Defaults below assume Groq,
    # since it's free — change these if you're using a different provider.
    cheap_model: str = "groq/llama3-8b-8192"
    capable_model: str = "groq/llama3-70b-8192"

    # CORS
    allowed_origins: str = "http://localhost:3000"

    # Risk score thresholds
    risk_low_max: int = 30
    risk_medium_max: int = 60
    risk_high_max: int = 85

    @property
    def allowed_origins_list(self) -> list[str]:
        return [origin.strip() for origin in self.allowed_origins.split(",") if origin.strip()]


settings = Settings()
