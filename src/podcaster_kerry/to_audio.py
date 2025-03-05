from pyt2s.services import stream_elements

def to_audio(content, path):
    # Custom Voice
    data = stream_elements.requestTTS(content, stream_elements.Voice.Russell.value)

    with open(path, '+wb') as file:
        file.write(data)
