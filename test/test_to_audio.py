from podcaster_kerry import to_audio
from . import SAMPLE

def test_to_audio():
    import pyttsx3

    # Initialize the TTS engine
    engine = pyttsx3.init()

    # Set the rate at which the text should be spoken
    rate = engine.getProperty('rate')
    engine.setProperty('rate', rate-50)

    # Set the volume of the spoken text
    volume = engine.getProperty('volume')
    engine.setProperty('volume', volume+0.25)

    # Set the voice to use
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    print(voices)

    # Set the text to be spoken
    text = SAMPLE

    print(text)

    # Save the spoken text to an audio file
    engine.save_to_file(text, 'output.mp3')

    engine.runAndWait()

    # Disconnect the TTS engine
    engine.stop()