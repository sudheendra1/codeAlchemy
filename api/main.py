import os
import io
from flask import Flask, request, jsonify, send_file
from PIL import Image
import requests
from ibm_boto3 import client
from ibm_botocore.client import Config
from dotenv import load_dotenv
from ibm_function.process import process_image_for_ocr, process_pdf
from ibm_function.voice import speech_to_text, text_to_speech
from ibm_function.watsonassistant import send_to_assistant
from llm.llm import send_to_llm
from llm.llm1 import send_to_llm_code
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

load_dotenv()  

# IBM Cloud Object Storage Configuration
COS_ENDPOINT = os.getenv("ENDPOINT")
COS_API_KEY_ID = os.getenv("API_KEY")
COS_INSTANCE_CRN = os.getenv("INSTANCE_CRN")
COS_BUCKET_NAME = os.getenv("BUCKET_NAME")
llm_memory = None 


# Initialize IBM Cloud Object Storage Client
cos = client(
    "s3",
    ibm_api_key_id=COS_API_KEY_ID,
    ibm_service_instance_id=COS_INSTANCE_CRN,
    config=Config(signature_version="oauth"),
    endpoint_url=COS_ENDPOINT
)

@app.route("/upload", methods=["POST"])
def upload_and_process_with_llm():
    global llm_memory
    if "file" not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No file selected for upload"}), 400

    file_ext = os.path.splitext(file.filename)[1].lower()

    try:
        # Extract text based on file type
        if file_ext in [".png", ".jpeg", ".jpg"]:  # Image for OCR
            extracted_text = process_image_for_ocr(file)

        elif file_ext in [".md", ".txt"]:  # README or text file
            extracted_text = file.read().decode("utf-8")

        elif file_ext == ".pdf":  # PDF files
            extracted_text = process_pdf(file)["content"]

        else:  # Unsupported file types
            cos.upload_fileobj(
                file,
                COS_BUCKET_NAME,
                f"misc_files/{file.filename}"
            )
            return jsonify({
                "message": f"File {file.filename} uploaded successfully!",
                "note": "File type not explicitly handled but stored in Object Storage."
            }), 200

        # Send extracted text to the LLM
        if file_ext in [".png", ".jpeg", ".jpg"]:
            llm_response = send_to_llm_code(extracted_text)

        else:
          llm_response = send_to_llm(extracted_text)

        # Optionally, send the LLM response or the extracted text to Watson Assistant
        #assistant_response = send_to_assistant(llm_response.get("results", extracted_text))
        llm_memory = llm_response

        return jsonify({
            "message": f"File {file.filename} processed successfully!",
            "llm_processed_json": llm_response,
            #"assistant_response": assistant_response
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/chat", methods=["POST"])
def chat_with_assistant():
    """
    Flask endpoint to handle chat interactions with Watson Assistant.
    """
    global llm_memory
    data = request.json
    user_input = data.get("message")
    if not user_input:
        return jsonify({"error": "No message provided"}), 400

    try:
        # Use the send_to_assistant function
        #assistant_response = send_to_assistant(user_input)
        # make a send to llm call
        if llm_memory:  # Check if the LLM response exists in memory
            # Use the LLM response stored earlier as the prompt for the assistant
            user_input = f"Previous LLM response: {llm_memory['llm_processed_json']}\nUser Message: {user_input}"
        assistant_response = send_to_llm_code(user_input)
        return jsonify({"response": assistant_response}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/voice", methods=["POST"])
def voice_interaction():
    if "audio" not in request.files:
        return jsonify({"error": "No audio file provided"}), 400

    audio_file = request.files["audio"]

    try:
        # Step 1: Convert audio to text
        user_text = speech_to_text(audio_file)

        # Step 2: Send text to Watson Assistant
        assistant_reply = send_to_assistant(user_text)

        # Step 3: Convert assistant reply to audio
        audio_content = text_to_speech(assistant_reply)

        # Return audio response
        audio_output = io.BytesIO(audio_content)
        return send_file(audio_output, mimetype="audio/wav", as_attachment=True, download_name="response.wav")

    except Exception as e:
        return jsonify({"error": str(e)}), 500
        
if __name__ == "__main__":
    app.run(debug=True)
