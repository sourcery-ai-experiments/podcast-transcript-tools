import json
from pathlib import Path

from loguru import logger  # type: ignore[import-not-found]


def json_file_to_json_file(origin_file: str, destination_file: str) -> None:
    try:
        data = json.loads(Path(origin_file).read_text())
    except json.JSONDecodeError as e:
        e.add_note(origin_file)
        raise
    if "version" not in data or "segments" not in data:
        logger.warning(f"Non-spec JSON file: {origin_file}")
    Path(destination_file).write_text(
        data=json.dumps(
            data,
            indent=4,
        ),
    )
