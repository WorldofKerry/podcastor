from dataclasses import dataclass
import subprocess
from gtts import gTTS
import re

# American english voices with > 1 speaker. https://github.com/rhasspy/piper/blob/9b1c6397698b1da11ad6cca2b318026b628328ec/src/python_run/piper/voices.json#L4
KEY_TO_NUM_SPEAKERS = {"en_US-libritts-high": 904, "en_US-arctic-medium": 18, "en_US-l2arctic-medium": 24}

@dataclass
class Entry:
    speaker_id: int
    text: str

# Default values from https://github.com/rhasspy/piper/blob/master/src/cpp/piper.hpp
@dataclass
class PiperParameters:
    length_scale: float = 1.0 # Phenome length (lower if faster)
    noise_scale: float = 0.667 # Generator noise
    noise_w: float = 0.8 # Phonme width noise
    sentence_silence: float = 0.0 # Seconds of silence after each sentence

    def as_args(self) -> list[str]:
        return [
            "--length-scale", str(self.length_scale),
            "--noise-scale", str(self.noise_scale),
            "--noise-w", str(self.noise_w),
            "--sentence-silence", str(self.sentence_silence),
        ]

def _make_entries(content: str) -> list[Entry]:
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
        ret.append(Entry(speaker_id, content))
    return ret

def get_audio(content: str):
    results = _make_entries(content)
    model = "en_US-arctic-medium"
    num_speakers = KEY_TO_NUM_SPEAKERS[model]

    for i, entry in enumerate(results):
        if entry.speaker_id > num_speakers:
            print(f"Speaker ID {entry.speaker_id} is out of range for model {model}, modifiying to {entry.speaker_id % num_speakers}")
            entry.speaker_id = entry.speaker_id % num_speakers
        parameters = PiperParameters()
        command = ["piper",
                "--model", model,
                "--speaker", str(entry.speaker_id),
                "--output-file", f"outputs/output_{i}.wav",
                *parameters.as_args(),
                ]
        _ = subprocess.check_output(command, input=entry.text.encode())

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
