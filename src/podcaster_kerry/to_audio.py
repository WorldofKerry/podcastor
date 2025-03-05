import pyttsx3

def to_audio(content, path):
    print("to_audio", content[:20], len(content), path)
    engine = pyttsx3.init()
    engine.save_to_file(content , path)
    engine.runAndWait()
    print("done")