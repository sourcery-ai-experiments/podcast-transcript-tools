class InvalidHtmlError(ValueError):
    """The HTML does not conform to the expected format of a valid transcript.

    Specifically, when there are no <cite> or <time> tags in the file.
    """

    def __init__(self) -> None:
        super().__init__("The provided HTML file is not a valid transcript.")


class NoTranscriptFoundError(ValueError):
    """Failed to locate transcript blocks in the provided source.

    This may happen for an invalid or empty file.
    """

    def __init__(self) -> None:
        super().__init__(
            "The provided source does not contain a transcript or could not be parsed.",
        )
