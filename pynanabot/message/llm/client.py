from openai import OpenAI
from pynanabot.settings import env


def get_client() -> OpenAI:
    return OpenAI(
        api_key=env('LLM_API_KEY'),
        base_url=env('LLM_BASE_URL'),
    )
