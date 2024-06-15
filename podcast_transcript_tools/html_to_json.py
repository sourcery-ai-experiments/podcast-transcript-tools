import json
from pathlib import Path

from bs4 import BeautifulSoup


def _ts_to_secs(time_string: str) -> float:
    hours, minutes, seconds, milliseconds = map(
        int,
        time_string.replace(",", ":").split(":"),
    )
    return (hours * 3600) + (minutes * 60) + seconds + (milliseconds / 1000)


# See spec at:
# https://github.com/Podcastindex-org/podcast-namespace/blob/main/transcripts/transcripts.md
def _html_to_list(soup: BeautifulSoup) -> list[dict]:
    blocks = []
    # TODO: detect cite/time for conformance to spec.
    for child in soup.children:
        if child.name == "p":
            blocks.append(
                {
                    "startTime": 0.0,
                    "endTime": 0.0,
                    "body": child.text,
                }
            )
    return blocks
    return None


def html_to_podcast_dict(html_string: str) -> dict:
    soup = BeautifulSoup(html_string, "html.parser")

    return {
        "version": "1.0.0",
        "segments": _html_to_list(soup),
    }


def html_file_to_json_file(html_file: str, json_file: str) -> None:
    Path(json_file).write_text(
        data=json.dumps(
            html_to_podcast_dict(
                html_string=Path(html_file).read_text(),
            ),
            indent=4,
        ),
    )
