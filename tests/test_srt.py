from pathlib import Path

import pytest

from podcast_transcript_tools.srt_to_json import _ts_to_secs, srt_to_podcast_dict


def test__ts_to_secs():
    assert _ts_to_secs("00:00:00,0") == 0
    assert _ts_to_secs("00:01:31,123") == 91.123
    assert _ts_to_secs("02:01:31,0") == 7291
    with pytest.raises(ValueError):
        _ts_to_secs("abc")
    with pytest.raises(ValueError):
        _ts_to_secs("")


def test_srt_to_podcast_dict():
    srt_string = Path("tests/fixtures/Bloat.srt").read_text()
    transcript_dict = srt_to_podcast_dict(srt_string)
    print(transcript_dict)
    assert transcript_dict["version"] == "1.0.0"
    assert len(transcript_dict["segments"]) == 724
    assert (
        transcript_dict["segments"][0]["body"]
        == "Michael: Hello, and welcome to PostgresFM, a weekly show about"
    )
    assert transcript_dict["segments"][0]["startTime"] == 0.060
    assert transcript_dict["segments"][0]["endTime"] == 2.680
    assert transcript_dict["segments"][-1]["body"] == "Take care, Chelsea."
    assert transcript_dict["segments"][-1]["startTime"] == 2173.940
    assert transcript_dict["segments"][-1]["endTime"] == 2174.920
