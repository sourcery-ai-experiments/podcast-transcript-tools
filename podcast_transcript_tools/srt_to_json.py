import re
from json import dumps
from pathlib import Path

from podcast_transcript_tools.errors import InvalidSrtError

srt_block = re.compile(r"(\d+:\d+:\d+[,.]\d+)\s*-->\s*(\d+:\d+:\d+[,.]\d+)(\s*)(.*)", flags=re.S)


def _mts_to_secs_float(time_string: str) -> float:
    hours, minutes, seconds, milliseconds = map(
        int,
        time_string.replace(",", ":").replace(".", ":").split(":"),
    )
    return round((hours * 3600) + (minutes * 60) + seconds + (milliseconds / 1000), 3)


def _is_int(s):
    try:
        int(s)
    except ValueError:
        return False
    else:
        return True


# See spec at:
# https://github.com/Podcastindex-org/podcast-namespace/blob/main/transcripts/transcripts.md
def _srt_block_to_dict(block: str) -> dict | None:
    if match := srt_block.search(block):
        start = _mts_to_secs_float(match[1])
        end = _mts_to_secs_float(match[2])
        body = match[4].strip().replace("\n", " ")

        return {"startTime": start, "endTime": end, "body": body}
    elif len(block) > 1 and _is_int(block[:2]):
        # TOD0: append body to previous
        raise InvalidSrtError(block)
    raise InvalidSrtError(block)


def srt_to_podcast_dict(srt_string: str) -> dict:
    blocks = [
        item for item in srt_string.split("\n\n") if not item.isspace() and item != ""
    ]

    return {
        "version": "1.0.0",
        "segments": list(map(_srt_block_to_dict, blocks)),
    }


def srt_file_to_json_file(srt_file: str, json_file: str) -> None:
    srt_string = Path(srt_file).read_text()
    try:
        transcript_dict = srt_to_podcast_dict(srt_string)
    except InvalidSrtError as e:
        e.add_note(srt_file)
        raise

    Path(json_file).write_text(
        data=dumps(transcript_dict, indent=4),
    )
