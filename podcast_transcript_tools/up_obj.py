import json
import os
import sys
from pathlib import Path

from loguru import logger
from objective import Client

from podcast_transcript_tools.file_utils import list_files


def _read_json_and_map_id(file_path: str) -> dict[str, str]:
    data = json.loads(Path(file_path).read_text())
    data["id"] = data["metadata"]["guid"]
    return data


def main(source_path: str, objective_api_key: str) -> None:
    client = Client(api_key=objective_api_key)
    files = list_files(source_path, [])
    logger.info(f"Reading {len(files)} files")
    objects = list(map(_read_json_and_map_id, files))
    logger.info("Uploading objects")
    batch_results = client.object_store.upsert_objects(objects)
    logger.info(batch_results)
    Path("batch_results.json").write_text(json.dumps(batch_results, indent=4))


if __name__ == "__main__":
    if len(sys.argv) == 1:
        logger.error(
            "Usage: up_obj <source dir> <obj. key or OBJECTIVE_KEY env var>",
        )
        sys.exit(1)

    main(
        source_path=sys.argv[1],
        objective_api_key=(
            sys.argv[2] if len(sys.argv) == 3 else os.getenv("OBJECTIVE_KEY")  # noqa: PLR2004
        ),
    )
