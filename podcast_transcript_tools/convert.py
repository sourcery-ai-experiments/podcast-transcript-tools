import concurrent.futures
from os import walk
from pathlib import Path
from sys import argv

from loguru import logger


def list_files(directory: str) -> list[str]:
    file_paths = []  # List to store file paths
    for root, _, filenames in walk(directory):
        dirpath = Path(root)
        file_paths.extend(
            dirpath / filename
            for filename in filenames
            if not filename.startswith(".")
            and not filename.endswith(".pdf")
            and not filename.endswith(".octet-stream")
        )
    return file_paths


def read_first_line(file_path: str) -> str:
    try:
        with Path.open(file_path) as file:
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


def main(transcript_directory: str) -> None:
    file_paths = list_files(transcript_directory)
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
        # else:
        #     print(f"Unknown file type: {unknown_files[i]}")

    known_files = vtt_files + srt_files + html_files + json_files
    unknown_pods = [
        file_name.split("/")[-2]
        for file_name in unknown_files
        if file_name not in known_files
    ]
    logger.info(f"Found {len(vtt_files)} VTT files")
    logger.info(f"Found {len(srt_files)} SRT files")
    logger.info(f"Found {len(html_files)} HTML files")
    logger.info(f"Found {len(json_files)} JSON files")
    logger.warning(f"Unknown: {set(unknown_pods)}")


if __name__ == "__main__":
    main(argv[1])
