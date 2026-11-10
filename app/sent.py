
from sentence_transformers import SentenceTransformer
from llama_index import SimpleDirectoryReader
#from langchain_openai import OpenAIEmbeddings
from llama_index.readers.web import SimpleWebPageReader
import textwrap
from llama_index import Document
from PIL import Image
import pandas as pd
# import torch
import clip

class ChatBotPDFToSentenceEmbedding():
    def __init__(self):
        self.model = SentenceTransformer('BAAI/bge-large-en-v1.5')
        self.chunk_size = 1280

    def load_document(self, file_path):
        documents = SimpleDirectoryReader(input_files=[file_path]).load_data()
        return documents

    def extract_value_or_empty(self, dictionary, key):
        return dictionary.get(key, "")

    def chunk_text(self, text, chunk_size):
        return textwrap.wrap(text, chunk_size)

    def generate_embedding(self, list_of_text_data):
        
        document_meta_list = []
        for doc in list_of_text_data:
            text_chunks = self.chunk_text(doc["text"], self.chunk_size)
            embeddings = self.model.encode(text_chunks, normalize_embeddings=True)

            for idx, chunk in enumerate(text_chunks):
                page_label = self.extract_value_or_empty(doc['metadata'], 'page')
                document_meta = {
                               "fileName": doc["metadata"]['file_path'],
                               "textIdx": idx,
                               "pageLabel": page_label,
                               "text": doc["text"],
                               "embedding": embeddings[idx].tolist(),
                               }
                document_meta_list.append(document_meta)

        return document_meta_list

    def __call__(self, list_of_text_data):
        document_meta_list = self.generate_embedding(list_of_text_data)
        return document_meta_list