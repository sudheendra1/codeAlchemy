import os
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 import Features, ConceptsOptions
from dotenv import load_dotenv

load_dotenv() 

# Watson NLP Configuration
nlp_service = NaturalLanguageUnderstandingV1(
    version='2021-08-01',
    authenticator=os.getenv("WATSON_AUTH") 
)
nlp_service.set_service_url(os.getenv("WATSON_ENDPOINT"))

def analyze_readme_with_nlp(readme_content):
    response = nlp_service.analyze(
        text=readme_content,
        features=Features(
            concepts=ConceptsOptions(limit=5)
        )
    ).get_result()
    return response


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

