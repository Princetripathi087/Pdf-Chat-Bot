# import json
# import os
# from datetime import datetime
# import string
# from uuid import uuid4
# from openai import OpenAI
# import dotenv
# import pandas as pd
# import uvicorn
# from fastapi import FastAPI, File, UploadFile, HTTPException , Form
# from fastapi.middleware.cors import CORSMiddleware
# from app.database import MongoDB
# from app.sent import ChatBotPDFToSentenceEmbedding
# from app.schemas import chatbotQueryPayLoad
# from fastapi import APIRouter, Depends
# from .. import schemas, utils
# import requests
# import base64
# from typing import List
# from fastapi.responses import JSONResponse
# from sentence_transformers import SentenceTransformer
# from PIL import Image
# import fitz
# from tqdm import tqdm
# import pymupdf4llm

# from llama_index import VectorStoreIndex
# from llama_parse import LlamaParse





# dotenv.load_dotenv() 

# router = APIRouter()

# chatbot_embedding_generator=ChatBotPDFToSentenceEmbedding()
# mongo_db_engine = MongoDB()
# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY")) 
# api_key = "sk-proj-ZQksNOHbcfPuYDrbzUjrT3BlbkFJwxSxnLWYRtniH7cnY7Zu"
# image_embedding_model = SentenceTransformer("clip-ViT-B-32")

# ### API KEYS
# api_url = os.getenv("API_URL")
# bearer_token = os.getenv("BEARER_TOKEN")

# headers = {
#     "Content-Type": "application/json",
#     "Authorization": f"Bearer {bearer_token}",
# }
# ###LlamaParse for Excel
# #Define a function to load documents from an Excel file
# def load_documents_from_excel(file_path: str):
#     df = pd.read_excel(file_path)
#     documents = df.to_dict(orient='records')
    
#     return documents


# class Metadata:
#     def __init__(self, text, metadata):
#         self.page_content = text
#         self.metadata = metadata
#     def __repr__(self):
#         return f"Metadata(page_content='{self.page_content}', metadata='{self.metadata}')"

# @router.post("/chatbot_ingest/")
# async def upload_pdf(files: list[UploadFile] = File(...)):
#     response_messages = []
#     for file in tqdm(files):
#         try:

#             pdf_reader = fitz.open(stream=file.file.read(), filetype="pdf")
            
            
            
#             md_text = pymupdf4llm.to_markdown(pdf_reader, page_chunks=True)

            
#             doc_meta_list = chatbot_embedding_generator(md_text)
#             mongo_db_engine.insert_chatbot_embedding(doc_meta_list)
#             # for s_md_text in md_text:
#             #     #all_text.append(s_md_text["text"])
#             #     #all_text.append({"page_content":s_md_text["text"]})
#             #     #all_text.append(Metadata(s_md_text["text"]))
#             #     all_text.append(Metadata(s_md_text["text"],s_md_text["metadata"]))
#             response_messages.append(f"The file: {file.filename} has been successfully ingested and processed!")
            
#         except Exception as e:
#             response_messages.append(f"Failed to process file: {file.filename}. Error: {str(e)}")
    
#     return JSONResponse(content={"messages": response_messages})

# @router.post("/chatbot_query")
# async def chatbot_retrieval_generate(pay_load: chatbotQueryPayLoad):
#     context = pay_load.question
#     query_vector = chatbot_embedding_generator.model.encode(
#         context).tolist()
    
#     retrieved_results = mongo_db_engine.chatbot_hybrid_search(
#         query_vector=query_vector, query=context,limit=5)

#     if not retrieved_results:
#         return {
#             "status_code": 200,
#             "question": pay_load.question,
#             "answer": "No relevant results found.",
#             "score": None,
#             "uuid": str(uuid4())
#         }
    
#     prompt = utils.chatbot_generate_prompt(retrieved_results)
#     completion = client.chat.completions.create(
#         model='gpt-3.5-turbo',
#         messages=[
#             {'role': 'system',
#                 'content': prompt,
#              },
#             {"role": "user",
#                 "content": pay_load.question},
#             {"role": "user",
#                 "content":
#                 "The answer should follow below template: {Answer}"}
#         ],
#         temperature=0.2,
#         stream=False
#     )
#     answer = completion.choices[0].message.content
#     print(answer)
#     # return answer
#     return {
#         "status_code": 200,
#         "question": pay_load.question,
#         "answer": answer,
#         "score": None,  # You can add a relevant score if needed
#         "uuid": str(uuid4())
#     }














# import json
# import os
# from datetime import datetime
# import string
# from uuid import uuid4
# from openai import OpenAI
# import dotenv
# import pandas as pd
# import uvicorn
# from fastapi import FastAPI, File, UploadFile, HTTPException , Form
# from fastapi.middleware.cors import CORSMiddleware
# from app.database import MongoDB
# from app.sent import ChatBotPDFToSentenceEmbedding
# from app.schemas import chatbotQueryPayLoad
# from fastapi import APIRouter, Depends
# from .. import schemas, utils
# import requests
# import base64
# from typing import List
# from fastapi.responses import JSONResponse
# from sentence_transformers import SentenceTransformer
# from PIL import Image
# import fitz
# from tqdm import tqdm
# import pymupdf4llm

# from llama_index import VectorStoreIndex
# from llama_parse import LlamaParse

# dotenv.load_dotenv()

# router = APIRouter()

# chatbot_embedding_generator = ChatBotPDFToSentenceEmbedding()
# mongo_db_engine = MongoDB()
# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
# api_key = ""
# image_embedding_model = SentenceTransformer("clip-ViT-B-32")

# ### API KEYS
# api_url = os.getenv("API_URL")
# bearer_token = os.getenv("BEARER_TOKEN")

# headers = {
#     "Content-Type": "application/json",
#     "Authorization": f"Bearer {bearer_token}",
# }

# ### Function to read summary.txt
# def read_summary_text():
#     summary_file = "E:/Baarez/Automation/NBR_ChatBot/Shubham/Final_NBR_Chatbot/summary.txt"
#     if os.path.exists(summary_file):
#         try:
#             with open(summary_file, "r", encoding="utf-8") as f:
#                 return f.read().strip()  # Read and remove any trailing spaces/newlines
#         except Exception as e:
#             print(f"Error reading summary.txt: {e}")
#             return ""
#     return ""  # Return empty string if file doesn't exist


# @router.post("/chatbot_ingest/")
# async def upload_pdf(files: List[UploadFile] = File(...)):
#     response_messages = []
#     summary_text = read_summary_text()  # Read summary.txt before processing

#     for file in tqdm(files):
#         try:
#             # Read PDF content
#             pdf_reader = fitz.open(stream=file.file.read(), filetype="pdf")
#             md_text = pymupdf4llm.to_markdown(pdf_reader, page_chunks=True)

#             # Append summary text to extracted PDF text
#             if summary_text:
#                 print("Appending summary.txt content to PDF text...")
#                 for s_md_text in md_text:
#                     s_md_text["text"] += "\n\n" + summary_text  # Append summary content

#             # Process the modified text
#             doc_meta_list = chatbot_embedding_generator(md_text)
#             mongo_db_engine.insert_chatbot_embedding(doc_meta_list)

#             response_messages.append(f"The file: {file.filename} has been successfully ingested and processed!")

#         except Exception as e:
#             response_messages.append(f"Failed to process file: {file.filename}. Error: {str(e)}")

#     return JSONResponse(content={"messages": response_messages})


# @router.post("/chatbot_query")
# async def chatbot_retrieval_generate(pay_load: chatbotQueryPayLoad):
#     context = pay_load.question
#     query_vector = chatbot_embedding_generator.model.encode(
#         context).tolist()
    
#     retrieved_results = mongo_db_engine.chatbot_hybrid_search(
#         query_vector=query_vector, query=context,limit=5)

#     if not retrieved_results:
#         return {
#             "status_code": 200,
#             "question": pay_load.question,
#             "answer": "No relevant results found.",
#             "score": None,
#             "uuid": str(uuid4())
#         }
    
#     prompt = utils.chatbot_generate_prompt(retrieved_results)
#     completion = client.chat.completions.create(
#         model='gpt-3.5-turbo',
#         messages=[
#             {'role': 'system',
#                 'content': prompt,
#              },
#             {"role": "user",
#                 "content": pay_load.question},
#             {"role": "user",
#                 "content":
#                 "The answer should follow below template: {Answer}"}
#         ],
#         temperature=0.2,
#         stream=False
#     )
#     answer = completion.choices[0].message.content
#     print(answer)
#     # return answer
#     return {
#         "status_code": 200,
#         "question": pay_load.question,
#         "answer": answer,
#         "score": None,  # You can add a relevant score if needed
#         "uuid": str(uuid4())
#     }








# ##Original

# import json
# import os
# import subprocess
# from datetime import datetime
# import string
# from uuid import uuid4
# from openai import OpenAI
# import dotenv
# import pandas as pd
# import uvicorn
# from fastapi import FastAPI, File, UploadFile, HTTPException , Form
# from fastapi.middleware.cors import CORSMiddleware
# from app.database import MongoDB
# from app.sent import ChatBotPDFToSentenceEmbedding
# from app.schemas import chatbotQueryPayLoad
# from fastapi import APIRouter, Depends
# from .. import schemas, utils
# import requests
# import base64
# from typing import List
# from fastapi.responses import JSONResponse
# from sentence_transformers import SentenceTransformer
# from PIL import Image
# import fitz
# from tqdm import tqdm
# import pymupdf4llm
# import sys
# from llama_index import VectorStoreIndex
# from llama_parse import LlamaParse

# dotenv.load_dotenv()

# router = APIRouter()

# chatbot_embedding_generator = ChatBotPDFToSentenceEmbedding()
# mongo_db_engine = MongoDB()
# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
# api_key = ""
# image_embedding_model = SentenceTransformer("clip-ViT-B-32")

# ### API KEYS
# api_url = os.getenv("API_URL")
# bearer_token = os.getenv("BEARER_TOKEN")

# headers = {
#     "Content-Type": "application/json",
#     "Authorization": f"Bearer {bearer_token}",
# }

# ### Function to read summary.txt
# def read_summary_text():
#     summary_file = "E:/Baarez/Automation/NBR_ChatBot/Shubham/Final_NBR_Chatbot - Copy/summary.txt"
#     if os.path.exists(summary_file):
#         try:
#             with open(summary_file, "r", encoding="utf-8") as f:
#                 return f.read().strip()
#         except Exception as e:
#             print(f"Error reading summary.txt: {e}")
#             return ""
#     return ""

# @router.post("/chatbot_ingest/")
# async def upload_pdf(files: List[UploadFile] = File(...)):
#     response_messages = []
#     save_dir = "E:/Baarez/Automation/NBR_ChatBot/Shubham/Final_NBR_Chatbot - Copy/PDF_Doc"
#     os.makedirs(save_dir, exist_ok=True)  # Ensure the folder exists
    
#     for file in files:
#         file_path = os.path.join(save_dir, file.filename)
#         with open(file_path, "wb") as f:
#             f.write(await file.read())  # Save file to PDF_Doc folder
    
#     print("Executing image.py...")
#     #subprocess.run(["python", "image.py"], check=True)
#     subprocess.run([sys.executable, "E:/Baarez/Automation/NBR_ChatBot/Shubham/Final_NBR_Chatbot - Copy/image.py"], check=True)
    
#     print("Executing imageSummary.py...")
#     #subprocess.run(["python", "ImageSummary.py"], check=True)
#     subprocess.run([sys.executable, "E:/Baarez/Automation/NBR_ChatBot/Shubham/Final_NBR_Chatbot - Copy/ImageSummary.py"], check=True)
    
#     summary_text = read_summary_text()  # Read summary.txt after executing scripts
    
#     for file in tqdm(files):
#         try:
#             file_path = os.path.join(save_dir, file.filename)
#             pdf_reader = fitz.open(file_path)
#             md_text = pymupdf4llm.to_markdown(pdf_reader, page_chunks=True)

#             if summary_text:
#                 print("Appending summary.txt content to PDF text...")
#                 for s_md_text in md_text:
#                     s_md_text["text"] += "\n\n" + summary_text

#             doc_meta_list = chatbot_embedding_generator(md_text)
#             mongo_db_engine.insert_chatbot_embedding(doc_meta_list)
#             response_messages.append(f"The file: {file.filename} has been successfully ingested and processed!")

#         except Exception as e:
#             response_messages.append(f"Failed to process file: {file.filename}. Error: {str(e)}")

#     return JSONResponse(content={"messages": response_messages})








# @router.post("/chatbot_query")
# async def chatbot_retrieval_generate(pay_load: chatbotQueryPayLoad):
#     context = pay_load.question
#     query_vector = chatbot_embedding_generator.model.encode(
#         context).tolist()
    
#     retrieved_results = mongo_db_engine.chatbot_hybrid_search(
#         query_vector=query_vector, query=context,limit=5)

#     if not retrieved_results:
#         return {
#             "status_code": 200,
#             "question": pay_load.question,
#             "answer": "No relevant results found.",
#             "score": None,
#             "uuid": str(uuid4())
#         }
    
#     prompt = utils.chatbot_generate_prompt(retrieved_results)
#     completion = client.chat.completions.create(
#         model='gpt-3.5-turbo',
#         messages=[
#             {'role': 'system',
#                 'content': prompt,
#              },
#             {"role": "user",
#                 "content": pay_load.question},
#             {"role": "user",
#                 "content":
#                 "The answer should follow below template: {Answer}"}
#         ],
#         temperature=0.2,
#         stream=False
#     )
#     answer = completion.choices[0].message.content
#     print(answer)
#     # return answer
#     return {
#         "status_code": 200,
#         "question": pay_load.question,
#         "answer": answer,
#         "score": None,  # You can add a relevant score if needed
#         "uuid": str(uuid4())
#     }







###adding arabic

import json
import os
import subprocess
from datetime import datetime
import string
from uuid import uuid4
from openai import OpenAI
import dotenv
import pandas as pd
import uvicorn
from fastapi import FastAPI, File, UploadFile, HTTPException , Form
from fastapi.middleware.cors import CORSMiddleware
from app.database import MongoDB
from app.sent import ChatBotPDFToSentenceEmbedding
from app.schemas import chatbotQueryPayLoad
from fastapi import APIRouter, Depends
from .. import schemas, utils
import requests
import base64
from typing import List
from fastapi.responses import JSONResponse
from sentence_transformers import SentenceTransformer
from PIL import Image
import fitz
from tqdm import tqdm
import pymupdf4llm
import sys
from llama_index import VectorStoreIndex
from llama_parse import LlamaParse
from langdetect import detect

from deep_translator import GoogleTranslator
import google.generativeai as genai

genai.configure(api_key="AIzaSyDfPHcVxzLrW267aj842fRps08OW70EBpI")
gemini_model = genai.GenerativeModel("gemini-1.5-flash")


dotenv.load_dotenv()

router = APIRouter()

chatbot_embedding_generator = ChatBotPDFToSentenceEmbedding()
mongo_db_engine = MongoDB()
#client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
client = OpenAI(api_key="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")  # ← your actual OpenAI API key

api_key = ""
image_embedding_model = SentenceTransformer("clip-ViT-B-32")

### API KEYS
api_url = os.getenv("API_URL")
bearer_token = os.getenv("BEARER_TOKEN")

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {bearer_token}",
}

### Function to read summary.txt
def read_summary_text():
    summary_file = "E:/Baarez/Automation/NBR_ChatBot/Shubham/Test/summary.txt"
    if os.path.exists(summary_file):
        try:
            with open(summary_file, "r", encoding="utf-8") as f:
                return f.read().strip()
        except Exception as e:
            print(f"Error reading summary.txt: {e}")
            return ""
    return ""

@router.post("/chatbot_ingest/")
async def upload_pdf(files: List[UploadFile] = File(...)):
    response_messages = []
    save_dir = "E:/Baarez/Automation/NBR_ChatBot/Shubham/Test/PDF_Doc"
    os.makedirs(save_dir, exist_ok=True)  # Ensure the folder exists
    
    for file in files:
        file_path = os.path.join(save_dir, file.filename)
        with open(file_path, "wb") as f:
            f.write(await file.read())  # Save file to PDF_Doc folder
    
    print("Executing image.py...")
    #subprocess.run(["python", "image.py"], check=True)
    subprocess.run([sys.executable, "E:/Baarez/Automation/NBR_ChatBot/Shubham/Test/image.py"], check=True)
    
    print("Executing imageSummary.py...")
    #subprocess.run(["python", "ImageSummary.py"], check=True)
    subprocess.run([sys.executable, "E:/Baarez/Automation/NBR_ChatBot/Shubham/Test/ImageSummary.py"], check=True)
    
    summary_text = read_summary_text()  # Read summary.txt after executing scripts
    
    for file in tqdm(files):
        try:
            file_path = os.path.join(save_dir, file.filename)
            pdf_reader = fitz.open(file_path)
            md_text = pymupdf4llm.to_markdown(pdf_reader, page_chunks=True)

            if summary_text:
                print("Appending summary.txt content to PDF text...")
                for s_md_text in md_text:
                    s_md_text["text"] += "\n\n" + summary_text

            doc_meta_list = chatbot_embedding_generator(md_text)
            mongo_db_engine.insert_chatbot_embedding(doc_meta_list)
            response_messages.append(f"The file: {file.filename} has been successfully ingested and processed!")

        except Exception as e:
            response_messages.append(f"Failed to process file: {file.filename}. Error: {str(e)}")

    return JSONResponse(content={"messages": response_messages})



from langdetect import detect
from googletrans import Translator

@router.post("/chatbot_query")
async def chatbot_retrieval_generate(pay_load: chatbotQueryPayLoad):
    original_question = pay_load.question
    language = detect(original_question)

    # If Arabic, translate to English
    if language == 'ar':
        translated_question = GoogleTranslator(source='auto', target='en').translate(original_question)
        query_vector = chatbot_embedding_generator.model.encode(translated_question).tolist()
        retrieved_results = mongo_db_engine.chatbot_hybrid_search(
            query_vector=query_vector, query=translated_question, limit=5)
        
        if not retrieved_results:
            return {
                "status_code": 200,
                "question": original_question,
                "answer": "لم يتم العثور على نتائج ذات صلة.",
                "score": None,
                "uuid": str(uuid4())
            }
        
        # Construct prompt with English context and original Arabic question
        context_prompt = utils.chatbot_generate_prompt(retrieved_results)
        final_prompt = f"""السؤال: {original_question}

السياق باللغة الإنجليزية:
{context_prompt}

الرجاء الإجابة على السؤال باللغة العربية باستخدام المعلومات أعلاه."""

        gemini_response = gemini_model.generate_content(final_prompt)
        arabic_answer = gemini_response.text.strip()

        # Save chat history logic can be added here
        return {
            "status_code": 200,
            "question": original_question,
            "answer": arabic_answer,
            "score": None,
            "uuid": str(uuid4())
        }

    # If not Arabic, proceed as usual
    query_vector = chatbot_embedding_generator.model.encode(original_question).tolist()
    retrieved_results = mongo_db_engine.chatbot_hybrid_search(
        query_vector=query_vector, query=original_question, limit=5)

    if not retrieved_results:
        return {
            "status_code": 200,
            "question": original_question,
            "answer": "No relevant results found.",
            "score": None,
            "uuid": str(uuid4())
        }

    prompt = utils.chatbot_generate_prompt(retrieved_results)
    completion = client.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=[
            {'role': 'system', 'content': prompt},
            {"role": "user", "content": original_question},
            {"role": "user", "content": "The answer should follow below template: {Answer}"}
        ],
        temperature=0.2,
        stream=False
    )
    answer = completion.choices[0].message.content
    return {
        "status_code": 200,
        "question": original_question,
        "answer": answer,
        "score": None,
        "uuid": str(uuid4())
    }



# @router.post("/chatbot_query")
# async def chatbot_retrieval_generate(pay_load: chatbotQueryPayLoad):
#     context = pay_load.question
#     query_vector = chatbot_embedding_generator.model.encode(
#         context).tolist()
    
#     retrieved_results = mongo_db_engine.chatbot_hybrid_search(
#         query_vector=query_vector, query=context,limit=5)

#     if not retrieved_results:
#         return {
#             "status_code": 200,
#             "question": pay_load.question,
#             "answer": "No relevant results found.",
#             "score": None,
#             "uuid": str(uuid4())
#         }
    
#     prompt = utils.chatbot_generate_prompt(retrieved_results)
#     completion = client.chat.completions.create(
#         model='gpt-3.5-turbo',
#         messages=[
#             {'role': 'system',
#                 'content': prompt,
#              },
#             {"role": "user",
#                 "content": pay_load.question},
#             {"role": "user",
#                 "content":
#                 "The answer should follow below template: {Answer}"}
#         ],
#         temperature=0.2,
#         stream=False
#     )
#     answer = completion.choices[0].message.content
#     print(answer)
#     # return answer
#     return {
#         "status_code": 200,
#         "question": pay_load.question,
#         "answer": answer,
#         "score": None,  # You can add a relevant score if needed
#         "uuid": str(uuid4())
#     }




