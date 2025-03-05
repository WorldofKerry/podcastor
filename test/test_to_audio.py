from podcaster_kerry import to_audio

def test_to_audio():
    SAMPLE = """
    H1: Hey, have you read that paper about the Tensor Processing Unit (TPU) from Google? It’s pretty fascinating how they’ve designed a custom ASIC specifically for neural network inference.  
    H2: Yeah, I did! It’s impressive how they managed to deploy it in their datacenters by 2015, just 15 months after starting the project. The TPU seems to be a game-changer for inference workloads.  

    H1: Absolutely. The heart of the TPU is this massive 65,536 8-bit MAC matrix multiply unit, which gives it a peak throughput of 92 TeraOps per second. That’s insane!  
    H2: Right? And they’ve got this 28 MiB software-managed on-chip memory. What’s interesting is how they’ve optimized for deterministic execution, which is crucial for meeting the 99th-percentile response-time requirements of their applications.  
    """
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

    assert False    