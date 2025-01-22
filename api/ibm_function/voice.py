import requests
import os

SPEECH_API_KEY = os.getenv("SPEECH_API_KEY")
SPEECH_URL = os.getenv("SPEECH_URL")
TEXT_API_KEY = os.getenv("TTS_API_KEY")
TEXT_URL = os.getenv("TTS_URL")


def speech_to_text(audio_file):
    try:
        stt_headers = {
            "Content-Type": "audio/wav",
            "Authorization": f"Bearer {SPEECH_API_KEY}",
        }
        response = requests.post(SPEECH_URL, headers=stt_headers, data=audio_file)
        response_data = response.json()

        if response.status_code != 200:
            raise Exception(response_data)

        # Extract text from response
        transcript = response_data.get("results", [])[0]["alternatives"][0]["transcript"]
        return transcript

    except Exception as e:
        raise Exception(f"Error in Speech to Text: {str(e)}")

def text_to_speech(text):
    try:
        tts_headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {TEXT_API_KEY}",
        }
        tts_payload = {
            "text": text,
            "voice": "en-US_AllisonV3Voice",
            "accept": "audio/wav",
        }
        response = requests.post(TEXT_URL, json=tts_payload, headers=tts_headers)

        if response.status_code != 200:
            raise Exception(response.json())

        return response.content

    except Exception as e:
        raise Exception(f"Error in Text to Speech: {str(e)}")