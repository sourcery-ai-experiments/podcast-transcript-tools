import json
from pathlib import Path

from loguru import logger  # type: ignore[import-not-found]

from podcast_transcript_tools.errors import NoStartTimeError


def _int_to_ts(seconds: int) -> str:
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return f"{hours:02}:{minutes:02}:{seconds:02}"


def _segment_to_line(segment: dict) -> str:
    try:
        start_time = _int_to_ts(segment["startTime"])
    except KeyError:
        raise NoStartTimeError
    try:
        speaker = f"{segment["speaker"]}: "
    except KeyError:
        speaker = ""
    return f"({start_time}) {speaker}{segment['body']}"


def json_file_to_simple_file(
    origin_file: str | Path,
    destination_file: str | Path,
) -> None:
    try:
        data = json.loads(Path(origin_file).read_text())
    except json.JSONDecodeError as e:
        e.add_note(origin_file)
        raise

    try:
        segments = map(_segment_to_line, data["segments"])
    except NoStartTimeError as e:
        e.add_note(origin_file)
        raise

    Path(destination_file).write_text("\n".join(segments))
