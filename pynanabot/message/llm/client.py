from django.conf import settings
from openai import OpenAI


def get_client() -> OpenAI:
    return OpenAI(
        api_key=settings.LLM_API_KEY,
        base_url=settings.LLM_BASE_URL,
    )
