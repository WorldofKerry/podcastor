from pyt2s.services import stream_elements

def to_audio(path):
    # Default Voice
    data = stream_elements.requestTTS('Lorem Ipsum is simply dummy text.')

    # Custom Voice
    data = stream_elements.requestTTS('Lorem Ipsum is simply dummy text.', stream_elements.Voice.Russell.value)

    with open(path, '+wb') as file:
        file.write(data)
