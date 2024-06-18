# podcast-transcript-tools

[![Lint and Test](https://github.com/hbmartin/podcast-transcript-tools/actions/workflows/lint.yml/badge.svg)](https://github.com/hbmartin/podcast-transcript-tools/actions/workflows/lint.yml)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Code style: black](https://img.shields.io/badge/🐧️-black-000000.svg)](https://github.com/psf/black)
[![Checked with pytype](https://img.shields.io/badge/🦆-pytype-437f30.svg)](https://google.github.io/pytype/)
[![twitter](https://img.shields.io/badge/@hmartin-00aced.svg?logo=twitter&logoColor=black)](https://twitter.com/hmartin)

Implementing indexing and conversion of podcast transcripts.

https://github.com/Podcastindex-org/podcast-namespace/blob/main/transcripts/transcripts.md

https://github.com/hbmartin/overcast-to-sqlite


## Usage

```bash
git clone git@github.com:hbmartin/podcast-transcript-tools.git
cd podcast-transcript-tools
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
# Replace with the actual path to your transcript files
python podcast_transcript_tools/convert.py ~/overcast-to-sqlite/archive/fixtures
```

## Authors
- [Harold Martin](https://www.linkedin.com/in/harold-martin-98526971/) - harold.martin at gmail
