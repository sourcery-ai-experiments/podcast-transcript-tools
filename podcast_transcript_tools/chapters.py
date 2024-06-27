import os
import sys
from pathlib import Path

from anthropic import Anthropic
from loguru import logger
from openai import OpenAI

from podcast_transcript_tools.json2simple import json_file_to_simple_file

ANTHROPIC_MODEL = os.environ.get("ANTHROPIC_MODEL") or "claude-3-opus-20240229"
GPT_MODEL = os.environ.get("GPT_MODEL") or "gpt-4-0125-preview"


def call_anthropic(api_key: str, prompt: str, temperature: float = 0.6) -> str:
    anthropic = Anthropic(api_key=api_key)

    request = anthropic.messages.create(
        model=ANTHROPIC_MODEL,
        max_tokens=3000,
        temperature=temperature,
        messages=[{"role": "user", "content": prompt}],
    )

    return request.content[0].text


def call_openai(api_key: str, prompt: str, temperature: float = 0.6) -> str:
    openai_client = OpenAI(api_key=api_key)
    result = openai_client.chat.completions.create(
        model=GPT_MODEL,
        temperature=temperature,
        messages=[{"role": "user", "content": prompt}],
    )
    return result.choices[0].message.content


def create_chapters(transcript: str) -> dict[str, str]:
    prompt = (
        "I'm going to give you a podcast transcript with timestamps in this format: "
        "`(00:00:00) Some transcription`. Generate a list of all major topics covered in the podcast, "
        "and the timestamp where the discussion starts. Make sure to use the timestamp BEFORE the the discussion "
        "starts. Make sure to cover topics from the whole episode. Use this format: `(00:00:00) Topic name`. "
        "Here's the transcript: \n\n"
        f"{transcript}"
    )

    claude_suggestions = call_anthropic(
        api_key=os.environ.get("ANTHROPIC_API_KEY"), prompt=prompt, temperature=0.6
    )
    gpt_suggestions = call_openai(
        api_key=os.environ.get("OPENAI_API_KEY"), prompt=prompt, temperature=0.6
    )

    return {"gpt": gpt_suggestions, "claude": claude_suggestions}


if __name__ == "__main__":
    if sys.argv[1].endswith(".simple"):
        source_path = Path(sys.argv[1])
    elif sys.argv[1].endswith(".json"):
        logger.info("Converting to simple format")
        source_path = Path(sys.argv[1].replace(".json", ".simple"))
        json_file_to_simple_file(sys.argv[1], source_path)
    else:
        print("Please provide a sSRT transcript file")
        sys.exit(1)
    chapters = create_chapters(Path(sys.argv[1]).read_text())
    for provider, suggestion in chapters.items():
        Path(str(source_path).replace(".simple", f".{provider}.chapters")).write_text(
            suggestion
        )
        logger.warning(provider)
        logger.info(suggestion)
    # TODO: write out suggestions to DB
