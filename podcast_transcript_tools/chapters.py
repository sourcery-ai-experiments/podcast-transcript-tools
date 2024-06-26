import os

from anthropic import Anthropic
from openai import BadRequestError, OpenAI

ANTHROPIC_MODEL = os.environ.get("ANTHROPIC_MODEL") or "claude-3-opus-20240229"
GPT_MODEL = os.environ.get("GPT_MODEL") or "gpt-4-0125-preview"


def call_anthropic(key: str, prompt: str, temperature: float = 0.5) -> str:
    try:
        anthropic = Anthropic(
            api_key=os.environ.get("ANTHROPIC_API_KEY"),
        )

        request = anthropic.messages.create(
            model=ANTHROPIC_MODEL,
            max_tokens=3000,
            temperature=temperature,
            messages=[{"role": "user", "content": prompt}],
        )

        return request.content[0].text
    except Exception as e:
        return f"An error occured with Claude: {e}"


def call_openai(key: str, prompt: str, temperature: float = 0.5) -> str:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    try:
        result = client.chat.completions.create(
            model=GPT_MODEL,
            temperature=temperature,
            messages=[{"role": "user", "content": prompt}],
        )
        return result.choices[0].message.content
    except BadRequestError as e:
        error_msg = f"An error occurred with OpenAI: {e}"
        print(error_msg)
        return error_msg


def create_chapters(transcript: str) -> tuple[str, str]:
    prompt = f"I'm going to give you a podcast transcript with timestamps for each speaker section in this format: `SPEAKER: Some transcription [00:00:00]`. Generate a list of all major topics covered in the podcast, and the timestamp where the discussion starts. Make sure to use the timestamp BEFORE the the discussion starts. Make sure to cover topics from the whole episode. Use this format: `- [00:00:00] Topic name`. Here's the transcript: \n\n {transcript}"

    claude_suggestions = call_anthropic(prompt, 0.6)
    gpt_suggestions = call_openai(prompt, 0.6)

    return gpt_suggestions, claude_suggestions


if __name__ == "__main__":
    anthropic_key = os.environ.get("ANTHROPIC_API_KEY")
    openai_key = os.environ.get("OPENAI_API_KEY")
    print(create_chapters("SPEAKER: Hello [00:00:00] SPEAKER: Hi [00:00:10]"))
