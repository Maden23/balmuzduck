from openai import OpenAI

client = OpenAI()

def text_to_speech(text):
    response = client.audio.speech.create(
        model="tts-1",
        voice="nova",
        input=text,
        response_format="opus"
    )
    response.stream_to_file("output.opus")

    return "output.opus"

def speech_to_text(audio_file):
    transcript = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file,
        response_format="text"
    )

    return transcript