import json
from pathlib import Path

import webvtt  # type: ignore[import-not-found]


def vtt_to_podcast_dict(vtt: webvtt.WebVTT) -> dict:
    # TODO: check timestamp types
    return {
        "version": "1.0.0",
        "segments": [
            {
                "startTime": caption.start,
                "endTime": caption.end,
                "body": caption.text,
            }
            for caption in vtt.captions
        ],
    }


# https://www.w3.org/TR/webvtt1/#file-structure
def vtt_file_to_json_file(vtt_file: str, json_file: str) -> None:
    Path(json_file).write_text(
        data=json.dumps(
            vtt_to_podcast_dict(
                webvtt.read(vtt_file),
            ),
            indent=4,
        ),
    )
