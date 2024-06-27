from collections.abc import Iterable

from .prompts import DEFAULT
from .providers import _ai_providers, ai_providers_list


def complete(
    prompts: dict[str, str],
    keys: dict[str, str],
    temperature: float = 0.6,
    providers: Iterable[str] | None = None,
) -> dict[str, str]:
    if providers is None:
        providers = ai_providers_list
    if keys is None:
        keys = {}

    results = {}

    for provider in providers:
        prompt = prompts.get(provider) or prompts.get(DEFAULT)
        model, call = _ai_providers[provider]
        results[provider] = call(keys[provider], model, prompt, temperature)

    return results
