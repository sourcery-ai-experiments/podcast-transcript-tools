import sys
from pathlib import Path

from loguru import logger

from podcast_transcript_tools.ai import (
    complete,
    prompt_transcript_to_chapters,
)
from podcast_transcript_tools.json2simple import json_file_to_simple_file


def create_chapters(transcript: str) -> dict[str, str]:
    return complete(
        prompts=prompt_transcript_to_chapters(transcript),
    )


if __name__ == "__main__":
    if sys.argv[1].endswith(".simple"):
        source_path = Path(sys.argv[1])
    elif sys.argv[1].endswith(".json"):
        logger.info("Converting to simple format")
        source_path = Path(sys.argv[1].replace(".json", ".simple"))
        json_file_to_simple_file(sys.argv[1], source_path)
    else:
        print("Please provide a simple transcript file")
        sys.exit(1)

    chapters = create_chapters(Path(sys.argv[1]).read_text())
    for provider, suggestion in chapters.items():
        Path(str(source_path).replace(".simple", f".{provider}.chapters")).write_text(
            suggestion,
        )
        logger.warning(provider)
        logger.info(suggestion)
    # TODO: write out suggestions to DB
