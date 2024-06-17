from functools import reduce
from json import dumps
from pathlib import Path
from typing import TYPE_CHECKING

from bs4 import BeautifulSoup, PageElement
from loguru import logger  # type: ignore[import-not-found]

from podcast_transcript_tools.errors import InvalidHtmlError, NoTranscriptFoundError

if TYPE_CHECKING:
    from collections.abc import Iterable


def _ts_to_secs(time_string: str) -> float:
    parts = enumerate(map(int, reversed(time_string.split(":"))))
    secs = next(parts)[1]
    return reduce(lambda acc, part: acc + ((60 ** part[0]) * part[1]), parts, secs)


# https://github.com/Podcastindex-org/podcast-namespace/blob/main/transcripts/transcripts.md#html
def _html_to_list(soup: BeautifulSoup) -> list[dict]:
    blocks: list[dict] = [{}]
    children: Iterable[PageElement] = soup.body.children if soup.body else soup.children  # type: ignore[attr-defined]
    for child in children:
        if child.name == "cite":  # type: ignore[attr-defined]
            if "speaker" not in blocks[-1]:
                blocks[-1]["speaker"] = child.text.replace(":", "").strip()
            else:
                blocks.append(
                    {
                        "speaker": child.text.replace(":", "").strip(),
                    },
                )
        elif child.name == "time":  # type: ignore[attr-defined]
            if "startTime" not in blocks[-1]:
                blocks[-1]["startTime"] = _ts_to_secs(child.text.strip())
            else:
                blocks.append(
                    {
                        "startTime": _ts_to_secs(child.text.strip()),
                    },
                )
        elif child.name == "p" and (stripped := child.text.strip()):  # type: ignore[attr-defined]
            blocks[-1]["body"] = stripped
    if len(blocks) == 1:
        raise NoTranscriptFoundError
    return blocks


def html_to_podcast_dict(html_string: str) -> dict:
    if "<cite>" not in html_string and "<time>" not in html_string:
        raise InvalidHtmlError

    soup = BeautifulSoup(html_string, "html.parser")

    return {
        "version": "1.0.0",
        "segments": _html_to_list(soup),
    }


def html_file_to_json_file(html_file: str, json_file: str) -> None:
    html_string = Path(html_file).read_text()
    try:
        transcript_dict = html_to_podcast_dict(html_string)
    except InvalidHtmlError:
        logger.error(f"No <cite> or <time> tags found in HTML file: {html_file}")
        return
    except NoTranscriptFoundError as e:
        e.add_note(html_file)
        raise

    Path(json_file).write_text(
        data=dumps(transcript_dict, indent=4),
    )
