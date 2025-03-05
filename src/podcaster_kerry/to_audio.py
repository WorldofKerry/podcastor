import pyttsx3
import time

def to_audio(content, path):
    print("to_audio", content[:100], len(content), path)
    engine = pyttsx3.init()
    engine.save_to_file(content[:100] , path)
    engine.runAndWait()
    time.sleep(20)
    print("done")