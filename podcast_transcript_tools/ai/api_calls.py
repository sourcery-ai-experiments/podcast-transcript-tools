import google.generativeai as gemini
from anthropic import Anthropic
from openai import OpenAI


def _call_anthropic(api_key: str, model: str, prompt: str, temperature: float) -> str:
    anthropic = Anthropic(api_key=api_key)

    request = anthropic.messages.create(
        model=model,
        max_tokens=3000,
        temperature=temperature,
        messages=[{"role": "user", "content": prompt}],
    )

    return request.content[0].text


def _call_openai(api_key: str, model: str, prompt: str, temperature: float) -> str:
    openai_client = OpenAI(api_key=api_key)
    result = openai_client.chat.completions.create(
        model=model,
        temperature=temperature,
        messages=[{"role": "user", "content": prompt}],
    )
    return result.choices[0].message.content


def _call_google(
    api_key: str, model: str, prompt: str, temperature: float,  # noqa: ARG001
) -> str:
    gemini.configure(api_key=api_key)
    model = gemini.GenerativeModel(model)

    response = model.generate_content(prompt)

    return response.text
