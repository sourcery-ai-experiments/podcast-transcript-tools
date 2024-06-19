from json import dumps
from pathlib import Path

import webvtt  # type: ignore[import-not-found]
from webvtt.errors import MalformedFileError

from podcast_transcript_tools.errors import InvalidVttError
from podcast_transcript_tools.srt_to_json import _mts_to_secs_float


def vtt_to_podcast_dict(vtt_string: str) -> dict:
    try:
        vtt = webvtt.from_string(vtt_string)
    except MalformedFileError as e:
        raise InvalidVttError from e
    return {
        "version": "1.0.0",
        "segments": [
            (
                {
                    "startTime": _mts_to_secs_float(caption.start),
                    "endTime": _mts_to_secs_float(caption.end),
                    "body": caption.text.strip().replace("\n", " "),
                    "speaker": caption.voice,
                }
                if caption.voice
                else {
                    "startTime": _mts_to_secs_float(caption.start),
                    "endTime": _mts_to_secs_float(caption.end),
                    "body": caption.text.strip().replace("\n", " "),
                }
            )
            for caption in vtt.captions
        ],
    }


# https://www.w3.org/TR/webvtt1/#file-structure
def vtt_file_to_json_file(vtt_file: str, json_file: str) -> None:
    vtt_string = Path(vtt_file).read_text()
    try:
        transcript_dict = vtt_to_podcast_dict(vtt_string)
    except InvalidVttError as e:
        e.add_note(vtt_file)
        raise
    Path(json_file).write_text(
        data=dumps(transcript_dict, indent=4),
    )
