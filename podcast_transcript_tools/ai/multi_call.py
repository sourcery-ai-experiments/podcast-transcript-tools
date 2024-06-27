from collections.abc import Iterable

from .prompts import DEFAULT
from .providers import AI_CALL, ai_calls, get_env_keys


def complete(
    prompts: dict[str, str],
    keys: dict[str, str] | None = None,
    temperature: float = 0.6,
    calls: Iterable[AI_CALL] | None = None,
) -> dict[str, str]:
    if calls is None:
        calls = ai_calls
    if keys is None:
        keys = get_env_keys({provider for provider, _, _ in calls})

    results = {}

    for provider, model, model_call in calls:
        prompt = prompts.get(model) or prompts.get(DEFAULT)
        results[provider] = model_call(keys[provider], model, prompt, temperature)

    return results
