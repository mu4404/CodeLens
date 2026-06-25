from app.core.config import settings
from app.services import openai_provider


def generate_code_review(diff_text: str) -> dict:
    if settings.llm_provider == "openai":
        return openai_provider.generate_code_review(diff_text)

    raise ValueError(f"지원하지 않는 LLM provider: {settings.llm_provider}")