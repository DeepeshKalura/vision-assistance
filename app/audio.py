import os
from dotenv import find_dotenv
from openai import OpenAI

from app.utility import cet

find_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


class RealTimeAudio:
    def __init__(self):
        self.client = OpenAI(os.getenv("OPENAI_API_KEY"))
    

    def start_transcribe(self):
        pass

    def stop_transcribe(self):
        pass

    def response(self):
        pass
    def generate_audio(self):
        pass


@cet
def generate_audio(text: str, name: str):
    """
    Generates audio from the given text using the Text-to-Speech API.

    Args:
        text (str): The text to convert into audio.
        name (str): The name of the file to save the audio as.

    Returns:
        None
    """
    response = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=text,
    )
    
    with client.audio.speech.with_streaming_response.create(
    model="tts-1",
    voice="alloy",
    input=text
    ) as response:
        response.stream_to_file(f"audio/{name}.mp3")

        

