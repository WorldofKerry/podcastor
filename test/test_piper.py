from podcaster_kerry.to_audio import get_audio
import subprocess
from . import SAMPLE

def test_create_piper_json():
    get_audio(SAMPLE)
    assert False