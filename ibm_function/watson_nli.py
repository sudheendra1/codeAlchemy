import os
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 import Features, ConceptsOptions
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator 
from dotenv import load_dotenv

load_dotenv() 

#print(os.getenv("WATSON_AUTH"))

authenticator = IAMAuthenticator(os.getenv("WATSON_AUTH"))

# Watson NLP Configuration
nlp_service = NaturalLanguageUnderstandingV1(
    version='2021-08-01',
    authenticator=authenticator
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

resp = analyze_readme_with_nlp("An AI-powered interactive debugging assistant that enables developers to communicate directly with their codebase. By establishing a contextual understanding of the entire codebase and engaging in targeted dialogue with users, the system provides intelligent debugging support and problem resolution through a carefully designed agent pipeline.Traditional debugging processes are time-consuming and often require developers to manually trace through complex codebases to identify and fix issues. There's a need for an intelligent system that can understand the full context of a codebase, interact naturally with developers, and provide accurate solutions while ensuring safety through verification steps")
print(resp)