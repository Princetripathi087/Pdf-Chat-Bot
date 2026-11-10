import os
from datetime import datetime
from uuid import uuid4
from openai import OpenAI
import dotenv
import uvicorn
#import boto3
from fastapi import FastAPI, File, UploadFile, HTTPException , Form
#from langchain_community.document_loaders import WebBaseLoader
from fastapi.middleware.cors import CORSMiddleware
from app.database import MongoDB
from app.sent import PDFToSentenceEmbedding, URLToSentenceEmbedding, textToSentenceEmbedding
from app.schemas import PayLoad,promptChat
from fastapi import APIRouter, Depends
from .. import schemas, utils
import requests

dotenv.load_dotenv() 

router = APIRouter()

embedding_generator = PDFToSentenceEmbedding()
url_embedding_generator = URLToSentenceEmbedding()
text_embedding_generator = textToSentenceEmbedding()
mongo_db_engine = MongoDB()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY")) 



### API KEYS
api_url = os.getenv("API_URL")
bearer_token = os.getenv("BEARER_TOKEN")

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {bearer_token}",
}


def write_string_to_temp_file(string: str) -> str:
    temp_filename = "temp_file.txt"
    file_path = f"./docs/{temp_filename}"

    with open(file_path, "w") as temp_file:
        temp_file.write(string)

    return file_path


#@router.post("/file_vector")
async def ingest_file(file: UploadFile = File(...)):

    try:
        save_file_path = utils.save_file(file=file)
        doc_meta_list = embedding_generator(save_file_path)
        os.remove(save_file_path)
        

        return doc_meta_list


    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
    

#@router.post("/url_vector")
async def scrapeURL(item : schemas.url):    
    url = item.url
    try:

        doc_meta_list = url_embedding_generator(url)


        return doc_meta_list

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


#@router.post("/text_vector")
async def text(item : schemas.text): 
    text = item.txt
    try:
        written_file = write_string_to_temp_file(text)
        doc_meta_list = text_embedding_generator(written_file)
        os.remove(written_file)

        return doc_meta_list
       

    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
    

#@router.post("/query_vector")
async def query_prompt(pay_load: PayLoad):
    context = pay_load.question 

    query_vector = embedding_generator.model.encode(
        context).tolist()
    
    return {"embedding":query_vector}