import os
from flask import Flask, request, jsonify
from ibm_boto3 import client
from ibm_botocore.client import Config
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv() 

#print(os.getenv("API_KEY"))

# IBM Cloud Object Storage Configuration
COS_ENDPOINT = os.getenv("ENDPOINT")   
COS_API_KEY_ID =  os.getenv("API_KEY")
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
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file part in the request"}), 400
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No file selected for upload"}), 400

    try:
        # Upload file to IBM Cloud Object Storage
        cos.upload_fileobj(
            file,
            COS_BUCKET_NAME,
            file.filename
        )
        return jsonify({"message": f"File {file.filename} uploaded successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
