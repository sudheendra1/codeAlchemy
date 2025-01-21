import os
from flask import Flask, request, jsonify
from PIL import Image
import pytesseract
import io
from ibm_boto3 import client
from ibm_botocore.client import Config
from dotenv import load_dotenv
from ibm_function.process import process_image_for_ocr, analyze_text_with_nlp, process_readme, process_pdf

app = Flask(__name__)

load_dotenv()  

# IBM Cloud Object Storage Configuration
COS_ENDPOINT = os.getenv("ENDPOINT")
COS_API_KEY_ID = os.getenv("API_KEY")
COS_INSTANCE_CRN = os.getenv("INSTANCE_CRN")
COS_BUCKET_NAME = os.getenv("BUCKET_NAME")

# Initialize IBM Cloud Object Storage Client
cos = client(
    "s3",
    ibm_api_key_id=COS_API_KEY_ID,
    ibm_service_instance_id=COS_INSTANCE_CRN,
    config=Config(signature_version="oauth"),
    endpoint_url=COS_ENDPOINT
)

@app.route("/upload", methods=["POST"])
def upload_and_process():
    if "file" not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No file selected for upload"}), 400

    file_ext = os.path.splitext(file.filename)[1].lower()

    try:
        if file_ext in [".png", ".jpeg", ".jpg"]:  # Image for OCR
            extracted_text = process_image_for_ocr(file)
            analysis_result = analyze_text_with_nlp(extracted_text)
            return jsonify({
                "message": f"Image {file.filename} processed successfully!",
                "extracted_text_preview": extracted_text[:500],
                "nlp_analysis": analysis_result
            }), 200

        elif file_ext in [".md", ".txt"]:  # README or text file
            result = process_readme(file)
            return jsonify(result), 200

        elif file_ext == ".pdf":  # PDF files
            result = process_pdf(file)
            return jsonify(result), 200

        else:  # Other files
            cos.upload_fileobj(
                file,
                COS_BUCKET_NAME,
                f"misc_files/{file.filename}"
            )
            return jsonify({
                "message": f"File {file.filename} uploaded successfully!",
                "note": "File type not explicitly handled but stored in Object Storage."
            }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
