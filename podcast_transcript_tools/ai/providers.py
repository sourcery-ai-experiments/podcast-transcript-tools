from collections.abc import Callable
from os import environ

from podcast_transcript_tools.ai.api_calls import _call_anthropic, _call_openai

OPENAI = "openai"
ANTHROPIC = "anthropic"

ANTHROPIC_MODEL = environ.get("ANTHROPIC_MODEL") or "claude-3-5-sonnet-20240620"
GPT_MODEL = environ.get("GPT_MODEL") or "gpt-4o-2024-05-13"

ai_providers: dict[str, Callable[[str, str, str, float], str]] = {
    OPENAI: (GPT_MODEL, _call_openai),
    ANTHROPIC: (ANTHROPIC_MODEL, _call_anthropic),
}

ai_providers_list = sorted(ai_providers.keys())


def get_env_keys() -> dict[str, str]:
    return {
        provider: environ.get(f"{provider.upper()}_API_KEY") or ""
        for provider in ai_providers_list
    }
