# podcast-transcript-tools

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
python podcast_transcript_tools/convert.py ~/Downloads/overcast-to-sqlite/archive/transcripts
```