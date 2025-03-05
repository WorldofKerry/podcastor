from gtts import gTTS

def to_audio(content, path):
    tts = gTTS(content)
    tts.save(path)
