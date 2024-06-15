import json
from pathlib import Path

import webvtt


def vtt_to_podcast_dict():
    pass


# https://www.w3.org/TR/webvtt1/#file-structure
def vtt_file_to_json_file(vtt_file: str, json_file: str) -> None:
    Path(json_file).write_text(
        data=json.dumps(
            vtt_to_podcast_dict(
                vtt_string=Path(vtt_file).read_text(),
            ),
            indent=4,
        ),
    )
