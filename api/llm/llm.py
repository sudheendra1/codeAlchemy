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
        "Authorization": f"Bearer eyJraWQiOiIyMDI0MTIzMTA4NDMiLCJhbGciOiJSUzI1NiJ9.eyJpYW1faWQiOiJJQk1pZC02OTcwMDBPUlJOIiwiaWQiOiJJQk1pZC02OTcwMDBPUlJOIiwicmVhbG1pZCI6IklCTWlkIiwianRpIjoiZGI3NGQwNmMtMjM3MC00NjQ5LTk2N2QtZGFlZDU3MDFmMmJlIiwiaWRlbnRpZmllciI6IjY5NzAwME9SUk4iLCJnaXZlbl9uYW1lIjoiTXVzdGFmYSIsImZhbWlseV9uYW1lIjoiQWtvbGF3YWxhIiwibmFtZSI6Ik11c3RhZmEgQWtvbGF3YWxhIiwiZW1haWwiOiJtdXN0dWFrb2xhQGdtYWlsLmNvbSIsInN1YiI6Im11c3R1YWtvbGFAZ21haWwuY29tIiwiYXV0aG4iOnsic3ViIjoibXVzdHVha29sYUBnbWFpbC5jb20iLCJpYW1faWQiOiJJQk1pZC02OTcwMDBPUlJOIiwibmFtZSI6Ik11c3RhZmEgQWtvbGF3YWxhIiwiZ2l2ZW5fbmFtZSI6Ik11c3RhZmEiLCJmYW1pbHlfbmFtZSI6IkFrb2xhd2FsYSIsImVtYWlsIjoibXVzdHVha29sYUBnbWFpbC5jb20ifSwiYWNjb3VudCI6eyJ2YWxpZCI6dHJ1ZSwiYnNzIjoiZGNhYTZhOWYwYzA5NDNkYzg3NmI5ODA2ZTAwN2JhOTIiLCJmcm96ZW4iOnRydWV9LCJpYXQiOjE3Mzc2MjE3NjcsImV4cCI6MTczNzYyNTM2NywiaXNzIjoiaHR0cHM6Ly9pYW0uY2xvdWQuaWJtLmNvbS9pZGVudGl0eSIsImdyYW50X3R5cGUiOiJ1cm46aWJtOnBhcmFtczpvYXV0aDpncmFudC10eXBlOmFwaWtleSIsInNjb3BlIjoiaWJtIG9wZW5pZCIsImNsaWVudF9pZCI6ImRlZmF1bHQiLCJhY3IiOjEsImFtciI6WyJwd2QiXX0.j5YGErZulWxOZ0izEmbdsENqkRd5wrTW86_Aq37B_KiWgEjcI9-MZwMmJb0oP-PLSFf6ultbzE2sSNFakZm2ItvdLqCFKVHgKV1xbRZ5J_eU7apkufNJs9b-v7fCbL9L_tT7e-reYkagXutJnatHo2N1yWxKx8H3BqVB-Ifuwq3V74vEhL4Cp4N0t_XgZK1-_Ogik9He98eh8vhdRsdLUIpfWpRr2QQkj8oGCF34M8mq9NRlHSCrdkcoUn79G7uNhZbaYx9dkZRxg2ty9vH1bnbLXIEiiIhD-ztJ3DnZrOVptfe_i8D4b2oYvVVAtdeoZdUHxprsSGYbw38Oqhr9XQ"
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