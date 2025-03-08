from dataclasses import dataclass
from enum import Enum
from pathlib import Path
import subprocess
import wave
import re
from pydub import AudioSegment
import torch
from TTS.api import TTS

SEGMENTS_DIR = "segments"
WAVE_FILE = "combined.wav"

# American english voices with > 1 speaker. https://github.com/rhasspy/piper/blob/9b1c6397698b1da11ad6cca2b318026b628328ec/src/python_run/piper/voices.json#L4
KEY_TO_NUM_SPEAKERS = {"en_US-libritts-high": 904, "en_US-arctic-medium": 18, "en_US-l2arctic-medium": 24}

@dataclass
class Entry:
    speaker_id: int
    text: str

class Engine(Enum):
    PIPER = "piper"
    COQUI = "coqui"

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

def _dialogue_as_entries(content: str) -> list[Entry]:
    ret = []
    parsed = _dialogue_as_list(content)
    speaker_mapping: dict[str, int] = {}
    id_counter = 0

    for speaker, content in parsed:
        if speaker not in speaker_mapping:
            speaker_mapping[speaker] = id_counter
            id_counter += 1
        speaker_id = speaker_mapping[speaker]
        ret.append(Entry(speaker_id, content))
    return ret

def dialogue_to_mp3(content: str, working_dir: Path, output: Path, engine: Engine = Engine.PIPER):
    segments_dir = working_dir / SEGMENTS_DIR

    working_dir.mkdir(parents=True, exist_ok=True)
    segments_dir.mkdir(parents=True, exist_ok=True)

    results = _dialogue_as_entries(content)

    match engine:
        case Engine.COQUI:
            _dialogue_to_mp3_coqui(results, segments_dir)
        case Engine.PIPER:
            _dialogue_to_mp3_piper(results, segments_dir)
        case _:
            raise ValueError(f"Unsupported engine {engine}")     
    
    _combine_wav_files(segments_dir, working_dir / WAVE_FILE)
    _wav_to_mp3(working_dir / WAVE_FILE, output)

def _dialogue_to_mp3_piper(entries: list[Entry], segments_dir: Path):
    model = "en_US-arctic-medium"
    num_speakers = KEY_TO_NUM_SPEAKERS[model]

    for entry in entries:
        if entry.speaker_id > num_speakers:
            print(f"Speaker ID {entry.speaker_id} is out of range for model {model}, modifiying to {entry.speaker_id % num_speakers}")
            entry.speaker_id = entry.speaker_id % num_speakers
        parameters = PiperParameters(length_scale=0.85)
        command = ["piper",
                "--model", model,
                "--speaker", str(entry.speaker_id),
                "--output-dir", str(segments_dir),
                "--update-voices",
                *parameters.as_args(),
                ]
        _ = subprocess.check_output(command, input=entry.text.encode())

def _dialogue_to_mp3_coqui(entries: list[Entry], segments_dir: Path):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)
    SPEAKERS = [(0, 'Claribel Dervla'), (1, 'Daisy Studious'), (2, 'Gracie Wise'), (3, 'Tammie Ema'), (4, 'Alison Dietlinde'), (5, 'Ana Florence'), (6, 'Annmarie Nele'), (7, 'Asya Anara'), (8, 'Brenda Stern'), (9, 'Gitta Nikolina'), (10, 'Henriette Usha'), (11, 'Sofia Hellen'), (12, 'Tammy Grit'), (13, 'Tanja Adelina'), (14, 'Vjollca Johnnie'), (15, 'Andrew Chipper'), (16, 'Badr Odhiambo'), (17, 'Dionisio Schuyler'), (18, 'Royston Min'), (19, 'Viktor Eka'), (20, 'Abrahan Mack'), (21, 'Adde Michal'), (22, 'Baldur Sanjin'), (23, 'Craig Gutsy'), (24, 'Damien Black'), (25, 'Gilberto Mathias'), (26, 'Ilkin Urbano'), (27, 'Kazuhiko Atallah'), (28, 'Ludvig Milivoj'), (29, 'Suad Qasim'), (30, 'Torcull Diarmuid'), (31, 'Viktor Menelaos'), (32, 'Zacharie Aimilios'), (33, 'Nova Hogarth'), (34, 'Maja Ruoho'), (35, 'Uta Obando'), (36, 'Lidiya Szekeres'), (37, 'Chandra MacFarland'), (38, 'Szofi Granger'), (39, 'Camilla Holmström'), (40, 'Lilya Stainthorpe'), (41, 'Zofija Kendrick'), (42, 'Narelle Moon'), (43, 'Barbora MacLean'), (44, 'Alexandra Hisakawa'), (45, 'Alma María'), (46, 'Rosemary Okafor'), (47, 'Ige Behringer'), (48, 'Filip Traverse'), (49, 'Damjan Chapman'), (50, 'Wulf Carlevaro'), (51, 'Aaron Dreschner'), (52, 'Kumar Dahl'), (53, 'Eugenio Mataracı'), (54, 'Ferran Simen'), (55, 'Xavier Hayasaka'), (56, 'Luis Moray'), (57, 'Marcos Rudaski')]
    for i, entry in enumerate(entries):
        entry.speaker_id += 23 # Dislike first speakers
        entry.speaker_id = entry.speaker_id % len(tts.speakers)
        tts.tts_to_file(
            text=entry.text,
            speaker=tts.speakers[entry.speaker_id],
            language="en",
            file_path=segments_dir / f"{i}.wav",
        )

def _combine_wav_files(segments: Path, output: Path):
    infiles = list(segments.glob("*.wav"))
    infiles.sort()
    if not infiles:
        raise ValueError(f"No audio files found in {segments}")
    data = []
    for infile in infiles:
        with wave.open(str(infile), "rb") as w:
            data.append([w.getparams(), w.readframes(w.getnframes())])
    with wave.open(str(output), "wb") as w:
        w.setparams(data[0][0])
        for i in range(len(data)):
            w.writeframes(data[i][1])

def _wav_to_mp3(wave_file: Path, mp3_file: Path):
    AudioSegment.from_wav(str(wave_file)).export(str(mp3_file), format="mp3")

def _dialogue_as_list(content: str) -> list[tuple[str, str]]:
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
    matches = re.findall(pattern, content, re.MULTILINE)
    return [(speaker, dialogue.strip()) for speaker, dialogue in matches]
