from typing import Dict, List
from app.config import settings
import pathlib
import os
import shutil
import json
import re
from passlib.context import CryptContext


TMP_DIR = "./docs"
os.makedirs(TMP_DIR, exist_ok=True)


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(password: str, hashed_password: str):
    return pwd_context.verify(password, hashed_password)




def save_file(file):
    file_path = f"{TMP_DIR}/{file.filename}"
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    return file_path


def mendix_generate_prompt(retrieved_results):
    context_dict = [{"sentence": item['text']}
                    for item in retrieved_results]

    context_json = json.dumps(context_dict)
    prompt = f"""
            Given the retrieved content in JSON format, please generate a concise and accurate answer to the following question, Provide the answer based only on the given context.
            - Do not add anything from your side.
            Retrieved document content: {context_json}
            """
    return prompt

def generate_prompt(retrieved_results):
    context_dict = [{"sentence": item['text'], "page number": item['pageLabel'],"file name": item['fileName']}
                    for item in retrieved_results]

    context_json = json.dumps(context_dict)
    prompt = f"""
            Given the retrieved document content with page numbers & file Name in JSON format, please generate a concise and accurate answer to the following question, including the page number where the evidence is found. Provide the answer based only on the given context.
            - Do not add anything from your side.
            - If the context is not relevant to the question or if there is no retrieved context, please return 'Unsatisfactory' followed by a statement explaining the lack of relevant evidence, including the content (if any) that was reviewed.
            - If the given context is sufficient to provide a satisfactory answer, please return 'Satisfactory' followed by the evidence context and the page number & file Name where the evidence is found.

            Retrieved document content: {context_json}
            """
    
    # prompt = "Given retrieved document content with page number in json format, please generate a concise and accurate answer to the following question with a page number to indicate where the evidence is. " + \
    #     "Please give answer from context only dont add anything else from your side if context is not relevent to quetion please return 'no relevant information found' "+\
    #     f"\n Retrieved document content: {context_json}"

    # prompt = "Given retrieved document content with page number in json format, please generate a concise and accurate answer to the following question with a page number to indicate where the evidence is. " + \
    #     f"\n Retrieved document content: {context_json}"
    
    return prompt



def chatbot_generate_prompt(retrieved_results):
    context_dict = [{"sentence": item['text'], "page number": item['pageLabel'],"file name": item['fileName']}
                    for item in retrieved_results]

    context_json = json.dumps(context_dict)
    # prompt = f"""
    #         Given the retrieved document content with page numbers & file Name in JSON format, please generate a concise and accurate answer to the following question, including the page number where the evidence is found. Provide the answer based only on the given context.
    #         - Do not add anything from your side.
    #         - If the context is not relevant to the question or if there is no retrieved context, please return 'Unsatisfactory' followed by a statement explaining the lack of relevant evidence, including the content (if any) that was reviewed.
    #         - If the given context is sufficient to provide a satisfactory answer, please return 'Satisfactory' followed by the evidence context and the page number & file Name where the evidence is found.

    #         Retrieved document content: {context_json}
    #         """
    
    # prompt = "Given retrieved document content with page number in json format, please generate a concise and accurate answer to the following question with a page number to indicate where the evidence is. " + \
    #     "Please give answer from context only dont add anything else from your side if context is not relevent to quetion please return 'no relevant information found' "+\
    #     f"\n Retrieved document content: {context_json}"

    prompt = "Given retrieved document content with page number in json format, please generate a concise and accurate answer to the following question" + \
        f"\n Retrieved document content: {context_json}"
    
    return prompt

def grc_generate_prompt(retrieved_results):
    context_dict = [{"sentence": item['text'], "page number": item['pageLabel'],"file name": item['fileName']}
                    for item in retrieved_results]

    context_json = json.dumps(context_dict)
    prompt = f"""
            Given the retrieved document content with page numbers & file Name in JSON format, please generate a concise and accurate answer to the following question, including the page number where the evidence is found. Provide the answer based only on the given context.
            - Do not add anything from your side.
            - If the context is not relevant to the question or if there is no retrieved context, please return 'Non-Compliant' followed by a statement explaining the lack of relevant evidence, including the content (if any) that was reviewed.
            - If the given context is sufficient to provide a satisfactory answer, please return 'Compliant' followed by the evidence context and the page number & file Name where the evidence is found.

            Retrieved document content: {context_json}
            """
    
    # prompt = "Given retrieved document content with page number in json format, please generate a concise and accurate answer to the following question with a page number to indicate where the evidence is. " + \
    #     "Please give answer from context only dont add anything else from your side if context is not relevent to quetion please return 'no relevant information found' "+\
    #     f"\n Retrieved document content: {context_json}"

    # prompt = "Given retrieved document content with page number in json format, please generate a concise and accurate answer to the following question with a page number to indicate where the evidence is. " + \
    #     f"\n Retrieved document content: {context_json}"
    
    return prompt

def grc_selfassesment_generate_prompt(retrieved_results):
    context_dict = [{"sentence": item['text'], "page number": item['pageLabel'],"file name": item['fileName']}
                    for item in retrieved_results]

    context_json = json.dumps(context_dict)
    prompt = f"""
            Given the retrieved document content with page numbers & file Name in JSON format, please generate a concise and accurate answer to the following question, including the page number where the evidence is found. Provide the answer based only on the given context.
            - Do not add anything from your side.
            - If the context is not relevant to the question or if there is no retrieved context, please return 'Non-Compliant' followed by a statement explaining the lack of relevant evidence, including the content (if any) that was reviewed.
            - If the given context is sufficient to provide a satisfactory answer, please return 'Compliant' followed by the evidence context and the page number & file Name where the evidence is found.

            Retrieved document content: {context_json}
            """
    
    # prompt = "Given retrieved document content with page number in json format, please generate a concise and accurate answer to the following question with a page number to indicate where the evidence is. " + \
    #     "Please give answer from context only dont add anything else from your side if context is not relevent to quetion please return 'no relevant information found' "+\
    #     f"\n Retrieved document content: {context_json}"

    # prompt = "Given retrieved document content with page number in json format, please generate a concise and accurate answer to the following question with a page number to indicate where the evidence is. " + \
    #     f"\n Retrieved document content: {context_json}"
    
    return prompt

def contract_generate_prompt(retrieved_results):
    context_dict = [{"sentence": item['text'], "page number": item['pageLabel'],"file name": item['fileName']}
                    for item in retrieved_results]

    context_json = json.dumps(context_dict)

    prompt = "Given retrieved document content with page number in json format, please generate a concise and accurate answer to the following question with a file name to indicate where the evidence is. " + \
        f"\n Retrieved document content: {context_json}"
    return prompt

def image_generate_prompt(retrieved_results: List[Dict]) -> str:
    breakpoint()
    # Create a list of dictionaries with relevant information from the retrieved results
    context_dict = [
        {
            "file name": item['fileName'],
            "score": item['score']
        }
        for item in retrieved_results
    ]

    # Convert the list of dictionaries to a JSON string
    context_json = json.dumps(context_dict, indent=2)

    # Construct the prompt
    prompt = (
        "Given the retrieved document content in JSON format, please generate a concise and accurate answer "
        "to the following question. Include the file name to indicate where the evidence is found.\n"
        f"Retrieved document content: {context_json}"
    )

    return prompt

def search_generate_prompt(retrieved_results):
    context_dict = [{"sentence": item['text'],"file name": item['fileName']}
                    for item in retrieved_results]

    context_json = json.dumps(context_dict)

    prompt = "Given retrieved document content with filename in json format, please generate a concise and accurate answer to the following question with a filename to indicate where the evidence is. " + \
        f"\n Retrieved document content: {context_json}"
    return prompt

def get_pag_number(string):

    page_number = 1
    pattern = "Page Number->(\d+)"
    founds = re.findall(pattern, string)

    if founds:
        try:
            page_number = int(founds[0])
        except IndexError:
            pass

    return page_number