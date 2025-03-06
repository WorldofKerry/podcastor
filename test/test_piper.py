from podcaster_kerry.to_audio import create_piper_json
from . import SAMPLE
import json

def test_create_piper_json():
    result = create_piper_json(SAMPLE)
    json_str = "\n".join(json.dumps(r) for r in result)
    print(json_str)

    assert False