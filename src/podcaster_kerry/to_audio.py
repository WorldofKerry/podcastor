from gtts import gTTS
import re

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
    result = parse_text(content)
    # FUTURE: https://stackoverflow.com/questions/37600197/custom-python-gtts-voice
    # Use localizations / accents to distinguish between different speakers
    tts = gTTS(content)
    tts.save(path)
