
import os
from pathlib import Path
from TTS.api import TTS
import torch
from podcaster_kerry.audio.helpers import Entry

os.environ["COQUI_TOS_AGREED"] = "1"

def _dialogue_to_mp3_coqui(entries: list[Entry], segments_dir: Path):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)
    for i, entry in enumerate(entries):
        entry.speaker_id += 23 # Dislike first speakers
        entry.speaker_id = entry.speaker_id % len(tts.speakers)
        tts.tts_to_file(
            text=entry.text,
            speaker=tts.speakers[entry.speaker_id],
            language="en",
            file_path=segments_dir / f"{i}.wav",
        )