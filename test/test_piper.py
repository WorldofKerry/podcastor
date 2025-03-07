import os
import shutil
from pathlib import Path
from podcaster_kerry.to_audio import get_audio
from . import SAMPLE
import pytest

# @pytest.mark.skipif(not os.getenv("GITHUB_ACTIONS"), reason="Only run on GitHub Actions")
def test_create_piper_json():
    temp_dir = Path("./outputs/")
    shutil.rmtree(temp_dir, ignore_errors=True)
    assert not temp_dir.exists()

    output = Path("./combined.mp3")
    output.unlink(missing_ok=True)
    assert not output.exists()

    get_audio(SAMPLE, temp_dir, output)

    assert temp_dir.exists()
    assert output.exists()
