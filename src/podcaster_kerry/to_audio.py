from gtts import gTTS
import re

def create_piper_json(content: str) -> list[dict]:
    """
    Return: follows format specified here: https://github.com/rhasspy/piper?tab=readme-ov-file#json-input
    { "text": "First speaker.", "speaker_id": 0, "output_file": "/tmp/speaker_0.wav" }
    """
    ret = []
    parsed = parse_text(content)
    speaker_mapping: dict[str, int] = {}
    id_counter = 0

    for speaker, content in parsed:
        if speaker not in speaker_mapping:
            speaker_mapping[speaker] = id_counter
            id_counter += 1
        speaker_id = speaker_mapping[speaker]
        ret.append({"text": content, "speaker_id": speaker_id})
    return ret

def parse_text(content: str) -> list[tuple[str, str]]:
    """
    ret[i] represents the i-th dialogue
    ret[i][0] is the speaker name
    ret[i][1] is the speaker content
    """
    content = content.strip() + "\n" # Ensure single newline at end
    pattern = r"(H\d):\s*(.*?)(?:\n(?=H\d:)|$)"
    print(content)
    matches = re.findall(pattern, content, re.MULTILINE)
    return [(speaker, dialogue.strip()) for speaker, dialogue in matches]

def to_audio(content, path):
    # FUTURE: https://stackoverflow.com/questions/37600197/custom-python-gtts-voice
    # Use localizations / accents to distinguish between different speakers
    tts = gTTS(content)
    tts.save(path)
