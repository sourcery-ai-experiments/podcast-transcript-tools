import concurrent.futures
import os
from sys import argv


def list_files(directory: str) -> list[str]:
    file_paths = []  # List to store file paths
    for dirpath, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            file_paths.append(
                os.path.join(dirpath, filename)
            )  # Append the file name to the full path
    return file_paths


def read_first_line(file_path: str) -> str:
    with open(file_path, "r") as file:
        return file.readline()


def read_files_in_parallel(file_paths: list[str]) -> list[str]:
    # Using ThreadPoolExecutor to handle multiple files in parallel
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Mapping the read_first_line function over all file paths
        results = executor.map(read_first_line, file_paths)
        return list(results)


def extract_file_types_from_name(
    file_paths: list[str],
) -> tuple[list[str], list[str], list[str], list[str]]:
    srt_files = []
    vtt_files = []
    html_files = []
    unknown_files = []

    for file_path in file_paths:
        if file_path.endswith(".vtt"):
            vtt_files.append(file_path)
        elif file_path.endswith(".srt"):
            srt_files.append(file_path)
        elif file_path.endswith((".htm", ".html")):
            html_files.append(file_path)
        else:
            unknown_files.append(file_path)
    return vtt_files, srt_files, html_files, unknown_files


def main(transcript_directory):
    file_paths = list_files(transcript_directory)
    vtt_files, srt_files, html_files, unknown_files = extract_file_types_from_name(
        file_paths
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
        # else:
        #     print(f"Unknown file type: {unknown_files[i]}")

    print(f"Found {len(vtt_files)} VTT files")
    print(f"Found {len(srt_files)} SRT files")
    print(f"Found {len(html_files)} HTML files")
    print(html_files)


if __name__ == "__main__":
    main(argv[1])
