from gtts import gTTS

def to_audio(content, path):
    # FUTURE: https://stackoverflow.com/questions/37600197/custom-python-gtts-voice
    # Use localizations / accents to distinguish between different speakers
    tts = gTTS(content)
    tts.save(path)
