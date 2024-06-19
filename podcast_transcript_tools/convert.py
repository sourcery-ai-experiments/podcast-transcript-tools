import concurrent.futures
from os import walk
from pathlib import Path
from sys import argv

from loguru import logger  # type: ignore[import-not-found]

from .html_to_json import html_file_to_json_file
from .json_to_json import json_file_to_json_file
from .srt_to_json import srt_file_to_json_file
from .vtt_to_json import vtt_file_to_json_file


def list_files(directory: str, ignore: list[str]) -> list[str]:
    file_paths: list[str] = []  # List to store file paths
    for root, _, filenames in walk(directory):
        dirpath = Path(root)
        file_paths.extend(
            str(dirpath / filename)
            for filename in filenames
            if not filename in ignore
            and not filename.startswith(".")
            and not filename.endswith(".pdf")
            and not filename.endswith(".octet-stream")
        )
    return file_paths


def read_first_line(file_path: str) -> str:
    try:
        with Path(file_path).open() as file:
            return file.readline()
    except ValueError as e:
        e.add_note(file_path)
        raise


def read_files_in_parallel(file_paths: list[str]) -> list[str]:
    # Using ThreadPoolExecutor to handle multiple files in parallel
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Mapping the read_first_line function over all file paths
        results = executor.map(read_first_line, file_paths)
        return list(results)


def extract_file_types_from_name(
    file_paths: list[str],
) -> tuple[list[str], list[str], list[str], list[str], list[str]]:
    srt_files = []
    vtt_files = []
    html_files = []
    json_files = []
    unknown_files = []

    for file_path in file_paths:
        if file_path.endswith(".vtt"):
            vtt_files.append(file_path)
        elif file_path.endswith(".srt"):
            srt_files.append(file_path)
        elif file_path.endswith((".htm", ".html")):
            html_files.append(file_path)
        elif file_path.endswith(".json"):
            json_files.append(file_path)
        else:
            unknown_files.append(file_path)
    return vtt_files, srt_files, html_files, json_files, unknown_files


def _destination_path(file_path: str, destination_dir: str) -> str:
    file_path = Path(file_path)
    parent = Path(destination_dir) / file_path.parts[-2]
    parent.mkdir(parents=True, exist_ok=True)
    return str(parent / (".".join(file_path.parts[-1].split(".")[:-1]) + ".json"))


def main(transcript_path: str, destination_path: str, ignore: list[str]) -> None:
    file_paths = list_files(transcript_path, ignore)
    (
        vtt_files,
        srt_files,
        html_files,
        json_files,
        unknown_files,
    ) = extract_file_types_from_name(
        file_paths,
    )
    # Enumerate first_lines and indentify any files matching patterns
    first_lines = read_files_in_parallel(unknown_files)
    for i, line in enumerate(first_lines):
        if "WEBVTT" in line:
            vtt_files.append(unknown_files[i])
        elif "1" in line:
            srt_files.append(unknown_files[i])
        elif "<" in line:
            html_files.append(unknown_files[i])
        elif "{" in line:
            json_files.append(unknown_files[i])

    known_files = vtt_files + srt_files + html_files + json_files
    unknown_pods = {
        file_name.split("/")[-2]
        for file_name in unknown_files
        if file_name not in known_files
    }
    logger.info(f"Found {len(vtt_files)} VTT files")
    logger.info(f"Found {len(srt_files)} SRT files")
    logger.info(f"Found {len(html_files)} HTML files")
    logger.info(f"Found {len(json_files)} JSON files")
    if len(unknown_pods) > 0:
        logger.warning(f"Unknown: {unknown_pods}")
    for vtt_file in vtt_files:
        vtt_file_to_json_file(vtt_file, _destination_path(vtt_file, destination_path))
    for srt_file in srt_files:
        srt_file_to_json_file(srt_file, _destination_path(srt_file, destination_path))
    for html_file in html_files:
        html_file_to_json_file(
            html_file, _destination_path(html_file, destination_path)
        )
    for json_file in json_files:
        json_file_to_json_file(
            json_file, _destination_path(json_file, destination_path)
        )


if __name__ == "__main__":
    if len(argv) < 4:  # noqa: PLR2004
        logger.error(
            "Usage: python convert.py <transcript source directory> <output directory>"
        )
    else:
        if len(argv) == 3:
            ignore = []
        else:
            ignore = Path(argv[3]).read_text().split("\n")
        main(transcript_path=argv[1], destination_path=argv[2], ignore=ignore)
