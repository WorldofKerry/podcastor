import os
import shutil
from pathlib import Path
from podcaster_kerry.to_audio import get_audio
from . import SAMPLE

def test_create_piper_json():
    if os.getenv("GITHUB_ACTIONS"):
        temp_dir = Path("./outputs/")
        shutil.rmtree(temp_dir, ignore_errors=True)
        assert not temp_dir.exists()

        output = Path("./combined.wav")
        output.unlink(missing_ok=True)
        assert not output.exists()

        get_audio(SAMPLE, temp_dir, output)

        assert temp_dir.exists()
        assert output.exists()
