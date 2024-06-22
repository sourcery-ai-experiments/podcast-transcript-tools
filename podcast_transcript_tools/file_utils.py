from collections.abc import Iterable
from concurrent.futures import ThreadPoolExecutor
from os import walk
from pathlib import Path


def _is_file_allowed(filename: str, ignore: list[str]) -> bool:
    return (
        filename not in ignore
        and not filename.startswith(".")
        and not filename.endswith(".pdf")
        and not filename.endswith(".octet-stream")
    )


def list_files(directory: str, ignore: list[str]) -> list[str]:
    file_paths: list[str] = []  # List to store file paths
    for root, _, filenames in walk(directory):
        dirpath = Path(root)
        file_paths.extend(
            str(dirpath / filename)
            for filename in filenames
            if _is_file_allowed(filename, ignore)
        )
    return file_paths


def _extract_file_types_from_name(
    file_paths: Iterable[str],
) -> tuple[list[str], list[str], list[str], list[str], list[str], list[str]]:
    srt_files = []
    vtt_files = []
    html_files = []
    json_files = []
    xml_files = []
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
        elif file_path.endswith((".xml", ".xsl")):
            xml_files.append(file_path)
        else:
            unknown_files.append(file_path)
    return vtt_files, srt_files, html_files, json_files, xml_files, unknown_files


def _read_first_line(file_path: str) -> str:
    try:
        with Path(file_path).open() as file:
            return file.readline()
    except ValueError as e:
        e.add_note(file_path)
        raise


def _read_files_in_parallel(file_paths: list[str]) -> list[str]:
    # Using ThreadPoolExecutor to handle multiple files in parallel
    with ThreadPoolExecutor() as executor:
        # Mapping the read_first_line function over all file paths
        results = executor.map(_read_first_line, file_paths)
        return list(results)


def _identify_file_types(
    file_paths: Iterable[str],
) -> tuple[list[str], list[str], list[str], list[str], list[str], set[str]]:
    (
        vtt_files,
        srt_files,
        html_files,
        json_files,
        xml_files,
        unknown_files,
    ) = _extract_file_types_from_name(
        file_paths,
    )
    # Enumerate first_lines and indentify any files matching patterns
    first_lines = _read_files_in_parallel(unknown_files)
    for i, line in enumerate(first_lines):
        if "WEBVTT" in line:
            vtt_files.append(unknown_files[i])
        elif "1" == line[0] or "-->" in line:
            srt_files.append(unknown_files[i])
        elif "<" in line:
            html_files.append(unknown_files[i])
        elif "{" in line and "rtf" not in line:
            json_files.append(unknown_files[i])
    known_files = vtt_files + srt_files + html_files + json_files
    unknown_pods = {
        file_name.split("/")[-2]
        for file_name in unknown_files
        if file_name not in known_files
    }
    return html_files, json_files, srt_files, vtt_files, xml_files, unknown_pods
