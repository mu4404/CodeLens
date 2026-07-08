from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """환경변수를 한 곳에서 타입 검증과 함께 관리합니다.

    os.getenv() 대신 이 클래스를 사용하면, 누락된 필수 값은
    서버 기동 시점에 즉시 에러로 드러납니다.
    """

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    # GitHub OAuth
    github_client_id: str = ""
    github_client_secret: str = ""

    # GitHub Webhook
    github_webhook_secret: str = ""

    # GitHub Bot Token
    github_bot_token: str = ""

    # JWT
    jwt_secret: str = ""

    # DB
    database_url: str = "postgresql+asyncpg://codelens:codelens@localhost:5432/codelens"

    # Redis
    redis_url: str = "redis://localhost:6379"

    # LLM Provider
    llm_provider: str = "openai"

    # OpenAI
    openai_api_key: str = ""

    # Anthropic
    anthropic_api_key: str = ""

    # 서비스
    frontend_url: str = "http://localhost:3000"
    webhook_base_url: str = "http://localhost:8000"


settings = Settings()
