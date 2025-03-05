import pyttsx3

def to_audio(content, path):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    for voice in voices:
        engine.setProperty('voice', voice.id)
        engine.say('The quick brown fox jumped over the lazy dog.')

    engine.runAndWait()

    engine.save_to_file(content , path)