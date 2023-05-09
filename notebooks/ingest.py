import openai
# Put anything you want in `API key`
openai.api_key = 'Free the models'

# Point to leapfrogai
openai.api_base = "https://leapfrogai.leapfrogai.bigbang.dev"
from langchain.embeddings import OpenAIEmbeddings

embeddings = OpenAIEmbeddings(openai_api_key="foobar",
                              openai_api_base="https://leapfrogai.leapfrogai.bigbang.dev",
                              model="text-embedding-ada-002")

print(print(openai.Model.list()))


from langchain.vectorstores import Weaviate
import weaviate
            
client = weaviate.Client(url="https://weaviate.leapfrogai.bigbang.dev",
                         additional_headers={
        'X-OpenAI-Api-Key': "foobar"
    })
client.schema.get()
client.get_meta()

schema = {
    "classes": [
        {
            "class": "Paragraph",
            "description": "A written paragraph",
            "vectorizer": "text2vec-transformers",
              "moduleConfig": {
                "text2vec-openai": {
                  "model": "ada",
                  "modelVersion": "002",
                  "type": "text"
                }
              },
            "properties": [
                {
                    "dataType": ["text"],
                    "description": "The content of the paragraph",
                    "moduleConfig": {
                        "text2vec-transformers": {
                          "skip": False,
                          "vectorizePropertyName": False
                        }
                      },
                    "name": "content",
                },
                {
                    "dataType": ["text"],
                    "description": "The source of the paragraph",
                    "moduleConfig": {
                        "text2vec-transformers": {
                          "skip": False,
                          "vectorizePropertyName": False
                        }
                      },
                    "name": "source",
                },
            ],
        },
    ]
}

# client.schema.create(schema)

vectordb = Weaviate(client, "Paragraph", "content", embedding=embeddings)

from langchain.document_loaders import UnstructuredMarkdownLoader, UnstructuredPDFLoader, UnstructuredHTMLLoader, UnstructuredFileLoader
from langchain.document_loaders import PyPDFLoader, CSVLoader, Docx2txtLoader, UnstructuredPowerPointLoader
from typing import List
from langchain.docstore.document import Document

from langchain.text_splitter import CharacterTextSplitter

import os

def load_file(file_path) -> List[Document]:
    _, file_extension = os.path.splitext(file_path)
    data: List[Document]
    if file_extension.lower() == '.html':
        loader = UnstructuredHTMLLoader(file_path)
        return loader.load()
    elif file_extension.lower() == '.pdf':
        loader = PyPDFLoader(file_path)
        return loader.load()
    elif file_extension.lower() == '.md':
        loader = UnstructuredMarkdownLoader(file_path)
        return loader.load()
    elif file_extension.lower() == '.csv':
        loader = CSVLoader(file_path)
        return loader.load()
    elif file_extension.lower() == '.pptx':
        loader = UnstructuredPowerPointLoader(file_path)
        return loader.load()
    elif file_extension.lower() == '.docx':
        loader = Docx2txtLoader(file_path)
        return loader.load()
    else:
        # Perform action for other files or skip
        return UnstructuredFileLoader(file_path).load()

def process_file(file_path, chunk_size=400, chunk_overlap=200):
    text_splitter = CharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    try:
        data = load_file(file_path=file_path)
        texts = text_splitter.split_documents(data)
        
        contents = [d.page_content for d in texts]
        metadatas = [d.metadata for d in texts] 
        vectordb.add_texts(
            texts=contents,
            metadatas=metadatas,
        )
         # split and load into weaviate
        print(f"Found { len(data) } parts in file { file_path}")
    except Exception as e: 
        print(f"process_file: Error parsing file { file_path}.  { e }")
        
   

def process_directory(folder_path):
    for root, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                process_file(file_path)
            except Exception as e:
                print(f"process_directory: Error processing file { file_path}: { e }")

process_directory("../data/")