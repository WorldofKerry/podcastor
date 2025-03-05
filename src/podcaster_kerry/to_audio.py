from gtts import gTTS
import time

def to_audio(content, path):
    print("to_audio", content[:100], len(content), path)
    tts = gTTS(content)
    tts.save(path)
    print("done")