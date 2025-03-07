from dataclasses import dataclass
from pathlib import Path
import subprocess
import wave
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
    ret = []
    parsed = _parse_text(content)
    speaker_mapping: dict[str, int] = {}
    id_counter = 0

    for speaker, content in parsed:
        if speaker not in speaker_mapping:
            speaker_mapping[speaker] = id_counter
            id_counter += 1
        speaker_id = speaker_mapping[speaker]
        ret.append(Entry(speaker_id, content))
    return ret

def get_audio(content: str, segments_dir: Path, output: Path):
    segments_dir.mkdir(parents=True, exist_ok=True)

    results = _make_entries(content)
    model = "en_US-arctic-medium"
    num_speakers = KEY_TO_NUM_SPEAKERS[model]

    for i, entry in enumerate(results):
        if entry.speaker_id > num_speakers:
            print(f"Speaker ID {entry.speaker_id} is out of range for model {model}, modifiying to {entry.speaker_id % num_speakers}")
            entry.speaker_id = entry.speaker_id % num_speakers
        parameters = PiperParameters(length_scale=0.85)
        command = ["piper",
                "--model", model,
                "--speaker", str(entry.speaker_id),
                "--output-file", str(segments_dir / f"audio_{i}.wav"),
                *parameters.as_args(),
                ]
        _ = subprocess.check_output(command, input=entry.text.encode())
    combine_audio(segments_dir, output)

def combine_audio(dir: Path, output: Path):
    infiles = list(dir.glob("*.wav"))
    infiles.sort()
    if not infiles:
        raise ValueError(f"No audio files found in {dir}")
    data = []
    for infile in infiles:
        with wave.open(str(infile), "rb") as w:
            data.append([w.getparams(), w.readframes(w.getnframes())])
    with wave.open(str(output), "wb") as w:
        w.setparams(data[0][0])
        for i in range(len(data)):
            w.writeframes(data[i][1])

def _parse_text(content: str) -> list[tuple[str, str]]:
    """
    Inputs:
    content in the format
    H1: blah blah blah
    H2: blah blah blah
    ...
    
    Returns:
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
