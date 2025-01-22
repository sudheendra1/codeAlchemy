import requests
import os

WATSON_ASSISTANT_API_KEY = os.getenv("WATSON_ASSISTANT_API_KEY")
WATSON_ASSISTANT_URL = os.getenv("WATSON_ASSISTANT_ENDPOINT")
WATSON_ASSISTANT_ID = os.getenv("WATSON_ASSISTANT_ID")

def send_to_assistant(user_input):
    """
    Sends user input to Watson Assistant and returns the assistant's response.
    """
    try:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {WATSON_ASSISTANT_API_KEY}"
        }
        payload = {
            "input": {
                "message_type": "text",
                "text": user_input
            }
        }
        url = f"{WATSON_ASSISTANT_URL}/v2/assistants/{WATSON_ASSISTANT_ID}/message?version=2022-04-01"
        response = requests.post(url, json=payload, headers=headers)
        response_data = response.json()

        if response.status_code != 200:
            raise Exception(f"Error from Watson Assistant: {response_data}")

        return response_data

    except Exception as e:
        raise Exception(f"Error in send_to_assistant: {str(e)}")