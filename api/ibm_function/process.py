import os
import io
from PIL import Image
import pytesseract
import pdfplumber
from ibm_botocore.client import Config
from ibm_boto3 import client
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 import Features, ConceptsOptions
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator 
from dotenv import load_dotenv

pytesseract.pytesseract.tesseract_cmd = 'C:\Program Files\Tesseract-OCR'

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

def process_image_for_ocr(file):
    """Process image file and extract text using OCR."""
    image = Image.open(io.BytesIO(file.read()))
    extracted_text = pytesseract.image_to_string(image)

    # Optionally save the OCR results in Object Storage
    cos.put_object(
        Bucket=COS_BUCKET_NAME,
        Key=f"ocr_results/{file.filename}.txt",
        Body=extracted_text
    )
    
    return extracted_text


authenticator = IAMAuthenticator(os.getenv("WATSON_AUTH"))
nlp_service = NaturalLanguageUnderstandingV1(
    version="2021-08-01",
    authenticator=authenticator
)
nlp_service.set_service_url(os.getenv("WATSON_ENDPOINT"))

def analyze_text_with_nlp(text_content):
    """
    Analyze any text content using Watson NLP.
    This function will be used for README, OCR results, PDF text, or any other text content.
    """
    try:
        response = nlp_service.analyze(
            text=text_content,
            features=Features(
                concepts=ConceptsOptions(limit=5)  # Customize options as needed
            )
        ).get_result()
        return response
    except Exception as e:
        return {"error": f"NLP Analysis Failed: {str(e)}"}

def process_pdf(file):
    """
    Process PDF file by extracting text and analyzing it with Watson NLP.
    """
    try:
        extracted_text = ""
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                extracted_text += page.extract_text() + "\n"

        # Save the extracted text in Object Storage
        cos.put_object(
            Bucket=COS_BUCKET_NAME,
            Key=f"pdf_results/{file.filename}.txt",
            Body=extracted_text
        )

        # Analyze the extracted text using Watson NLP
        analysis_result = analyze_text_with_nlp(extracted_text)

        return {
            "message": f"PDF {file.filename} processed successfully!",
            "extracted_text_preview": extracted_text[:500],  # First 500 characters
            "nlp_analysis": analysis_result
        }
    except Exception as e:
        return {"error": f"Failed to process PDF: {str(e)}"}

def process_readme(file):
    """
    Process README file by analyzing it with Watson NLP.
    """
    try:
        readme_content = file.read().decode("utf-8")

        # Save the README content in Object Storage
        cos.put_object(
            Bucket=COS_BUCKET_NAME,
            Key=f"readme_files/{file.filename}",
            Body=readme_content
        )

        # Analyze the content using Watson NLP
        analysis_result = analyze_text_with_nlp(readme_content)

        return {
            "message": f"README {file.filename} processed successfully!",
            "content_preview": readme_content[:500],  # First 500 characters
            "nlp_analysis": analysis_result
        }
    except Exception as e:
        return {"error": f"Failed to process README: {str(e)}"}
    
def parse_directory_structure(structure_text):
    directory_map = {}
    current_dir = None

    for line in structure_text.splitlines():
        if line.endswith(":"):  # Directory name
            current_dir = line[:-1]
            directory_map[current_dir] = []
        elif current_dir and line.strip():  # File in the current directory
            directory_map[current_dir].append(line.strip())

    return directory_map

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