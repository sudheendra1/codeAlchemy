import os
import json
import requests
from ibm_botocore.client import Config
from ibm_boto3 import client
from dotenv import load_dotenv

load_dotenv() 

# IBM COS Configuration
COS_ENDPOINT = os.getenv("ENDPOINT")   
COS_API_KEY_ID =  os.getenv("API_KEY")
COS_INSTANCE_CRN = os.getenv("INSTANCE_CRN")   
COS_BUCKET_NAME = os.getenv("BUCKET_NAME") 

# Initialize COS Client
cos = client(
    "s3",
    ibm_api_key_id=COS_API_KEY_ID,
    ibm_service_instance_id=COS_INSTANCE_CRN,
    config=Config(signature_version="oauth"),
    endpoint_url=COS_ENDPOINT
)

def parse_readme(file_key):
    try:
        # Download the README file
        response = cos.get_object(Bucket=COS_BUCKET_NAME, Key=file_key)
        readme_content = response["Body"].read().decode("utf-8")

        # Extract project description (basic example)
        lines = readme_content.split("\n")
        project_description = lines[0] if lines else "No description found."

        # Extract dependencies section (if exists)
        dependencies = []
        if "dependencies" in readme_content.lower():
            dependencies = [
                line.strip() for line in lines if "dependency" in line.lower()
            ]

        return {
            "project_description": project_description,
            "dependencies": dependencies
        }
    except Exception as e:
        return {"error": str(e)}

def main(params):
    file_key = params.get("file_key")
    if not file_key:
        return {"error": "No file key provided."}

    result = parse_readme(file_key)
    print(result)
    return result

main({"file_key": "README.md"})

