import requests
import os

api_key = os.getenv("WATSONX_API")


def send_to_llm(extracted_text):
    """
    Sends the extracted text to an LLM and returns the structured JSON response.
    """
    url = "https://eu-de.ml.cloud.ibm.com/ml/v1/text/generation?version=2023-05-29"
    
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer eyJraWQiOiIyMDI0MTIzMTA4NDMiLCJhbGciOiJSUzI1NiJ9.eyJpYW1faWQiOiJJQk1pZC02OTcwMDBPUlJOIiwiaWQiOiJJQk1pZC02OTcwMDBPUlJOIiwicmVhbG1pZCI6IklCTWlkIiwianRpIjoiNmZmYmY2NGUtOWU5YS00ZDZiLTgxM2EtOTQ3ODhiNmJiMDRiIiwiaWRlbnRpZmllciI6IjY5NzAwME9SUk4iLCJnaXZlbl9uYW1lIjoiTXVzdGFmYSIsImZhbWlseV9uYW1lIjoiQWtvbGF3YWxhIiwibmFtZSI6Ik11c3RhZmEgQWtvbGF3YWxhIiwiZW1haWwiOiJtdXN0dWFrb2xhQGdtYWlsLmNvbSIsInN1YiI6Im11c3R1YWtvbGFAZ21haWwuY29tIiwiYXV0aG4iOnsic3ViIjoibXVzdHVha29sYUBnbWFpbC5jb20iLCJpYW1faWQiOiJJQk1pZC02OTcwMDBPUlJOIiwibmFtZSI6Ik11c3RhZmEgQWtvbGF3YWxhIiwiZ2l2ZW5fbmFtZSI6Ik11c3RhZmEiLCJmYW1pbHlfbmFtZSI6IkFrb2xhd2FsYSIsImVtYWlsIjoibXVzdHVha29sYUBnbWFpbC5jb20ifSwiYWNjb3VudCI6eyJ2YWxpZCI6dHJ1ZSwiYnNzIjoiZGNhYTZhOWYwYzA5NDNkYzg3NmI5ODA2ZTAwN2JhOTIiLCJmcm96ZW4iOnRydWV9LCJpYXQiOjE3Mzc1NDc5ODIsImV4cCI6MTczNzU1MTU4MiwiaXNzIjoiaHR0cHM6Ly9pYW0uY2xvdWQuaWJtLmNvbS9pZGVudGl0eSIsImdyYW50X3R5cGUiOiJ1cm46aWJtOnBhcmFtczpvYXV0aDpncmFudC10eXBlOmFwaWtleSIsInNjb3BlIjoiaWJtIG9wZW5pZCIsImNsaWVudF9pZCI6ImRlZmF1bHQiLCJhY3IiOjEsImFtciI6WyJwd2QiXX0.nMwF__4XhTCDzg-0inuLrHg3YdTZLC6LEZqazbM14KQx-HAaE6kCEpPwQFVxp_ewt396fkSJZYLGLkU9W5T3iyMunIgfoX-bC7nY4dHyhFA7Tu1s2AnlvAOLXWmzagfumMtZCqwvrnNjeZxyvCAH6yp3eY60u8Ihhuvj1GmHHkBHZS8vaDWajxQCzhJ3yw0wfLHAVu4I9J9tALKbDwWOmlJbnNTCwm1L6ONGnqE9A2b0fUdpft0e00M2jsa-qzNI1qzmqWyGljf-oh2oJH4NYCMduw46Q9JSSr_rzkiGNOQTivkJhGt1NnfLnrmk3Najpp7TLJTeCayVb0l_Q0RvNQ"
    }
    body = {
        "input": (
        "Content:\n"
        f"{extracted_text}"
        "Extract knowledge from the following content and return it **ONLY** as a JSON object. "
        "The output should contain no narrative text, no explanations, and no bullet points—just the JSON object. "
        "The structure must strictly adhere to the following format:\n\n"
        "{\n"
        "  \"codebase_overview\": \"<Brief description of the project>\",\n"
        "  \"functions\": [\"<List of key functions or features>\"],\n"
        "  \"dependencies\": [\"<List of libraries or tools used>\"],\n"
        "  \"files\": [\"<List of key files in the project>\"],\n"
        "  \"user_query\": \"<Answer to the user's query>\"\n"
        "}\n\n"
        "*STOP* after the user query"
    ),
        "parameters": {
            "decoding_method": "greedy",
            "max_new_tokens": 200
        },
        "model_id": "ibm/granite-3-8b-instruct",
        "project_id": "984624f3-7be3-4258-9114-f99e75adef88"
    }
    response = requests.post(url, headers=headers, json=body)

    if response.status_code != 200:
        raise Exception(f"LLM API Error: {response.text}")
    
    return response.json()