DEFAULT = "default"


def prompt_transcript_to_chapters(transcript: str) -> dict[str, str]:
    default = (
        "I'm going to give you a podcast transcript with timestamps in this format: "
        "`(00:03:05) Some transcription`. with the timestamp in parentheses. "
        "Generate a list of all major topics covered in the podcast, "
        "and the timestamp where the discussion starts. Make sure to use the timestamp BEFORE the the discussion "
        "starts. Make sure to cover topics from the whole episode. Use this format: `(00:03:05) Topic name`. "
        "Do not write any preamble or text before the chapter list, only write the chapter list. "
        "Do not write anything before the timestamp in parentheses on each line. "
        "Here's the transcript: \n\n"
        f"{transcript}"
    )

    return {DEFAULT: default}
