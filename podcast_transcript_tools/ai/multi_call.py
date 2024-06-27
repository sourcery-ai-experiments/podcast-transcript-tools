from collections.abc import Iterable

from podcast_transcript_tools.ai import DEFAULT
from podcast_transcript_tools.ai.providers import ai_providers_list


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

    # TODO: make these calls parallel / async
    results = {}

    for provider in providers:
        prompt = prompts.get(provider) or prompts.get(DEFAULT)
        model, call = providers[provider]
        results[provider] = call(keys[provider], model, prompt, temperature)

    return results
