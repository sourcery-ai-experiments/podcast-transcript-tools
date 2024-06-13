import json
import re
from pathlib import Path

srt_block = re.compile(r"(\d+:\d+:\d+,\d+) --> (\d+:\d+:\d+,\d+)(\s*)(.*)", flags=re.S)


def _ts_to_secs(time_string: str) -> float:
    hours, minutes, seconds, milliseconds = map(
        int,
        time_string.replace(",", ":").split(":"),
    )
    return (hours * 3600) + (minutes * 60) + seconds + (milliseconds / 1000)


# See spec at:
# https://github.com/Podcastindex-org/podcast-namespace/blob/main/transcripts/transcripts.md
def _srt_block_to_dict(block: str) -> dict | None:
    if match := srt_block.search(block):
        start = _ts_to_secs(match[1])
        end = _ts_to_secs(match[2])
        body = match[4].strip().replace("\n", " ")

        return {"startTime": start, "endTime": end, "body": body}

    return None


def srt_to_podcast_dict(srt_string: str) -> dict:
    return {
        "version": "1.0.0",
        "segments": map(_srt_block_to_dict, srt_string.split("\n\n")),
    }


def srt_file_to_json_file(srt_file: str, json_file: str) -> None:
    Path(json_file).write_text(
        data=json.dumps(
            srt_to_podcast_dict(
                srt_string=Path(srt_file).read_text(),
            ),
            indent=4,
        ),
    )
