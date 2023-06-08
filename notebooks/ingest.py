import openai
import sys

import threading
from queue import Queue
import os
import sys
import multiprocessing
import time

# Put anything you want in `API key`
openai.api_key = 'Free the models'

# Point to leapfrogai
openai.api_base = "https://leapfrogai.dd.bigbang.dev"
from langchain.embeddings import OpenAIEmbeddings

embeddings = OpenAIEmbeddings(openai_api_key="foobar",
                              openai_api_base="https://leapfrogai.dd.bigbang.dev",
                              model="text-embedding-ada-002")

print(openai.Model.list())


from langchain.vectorstores import Weaviate
import weaviate
            
client = weaviate.Client(url="https://weaviate.dd.bigbang.dev",
                         additional_headers={
        'X-OpenAI-Api-Key': "foobar"
    })
# client.schema.get()
# client.get_meta()

schema = {
    "classes": [
        {
            "class": "Company",
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

client.schema.create(schema)

vectordb = Weaviate(client, "Company", "content", embedding=embeddings)

from langchain.document_loaders import UnstructuredMarkdownLoader, UnstructuredPDFLoader, UnstructuredHTMLLoader, UnstructuredFileLoader
from langchain.document_loaders import PyPDFLoader, CSVLoader, Docx2txtLoader, UnstructuredPowerPointLoader
from typing import List
from langchain.docstore.document import Document

from langchain.text_splitter import CharacterTextSplitter, TokenTextSplitter

import os

def clean_string(text):
    # Split the string by spaces.
    # This gives us a list where multi-spaces will be represented as ''.
    text_list = text.split(' ')

    # Rejoin with ' ' instead of ''
    cleaned_text = ''.join([' ' if x == '' else x for x in text_list ])
    return cleaned_text.replace("  ", " ")
def percentage_of_char(input_string, char):
    count_char = input_string.count(char)
    total_chars = len(input_string)
    percentage = (count_char / total_chars) * 100
    return percentage

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

def process_file(file_path, chunk_size=1000, chunk_overlap=400):
    # text_splitter = CharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    text_splitter = TokenTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    try:
        data = load_file(file_path=file_path)
        texts = text_splitter.split_documents(data)
        for t in texts:
            if percentage_of_char(t.page_content, ' ') > 25:
                print("REPLACING: ")
                print(t.page_content)
                print("WITH:")
                clean = clean_string(t.page_content)
                print(clean)
                print("---------")
                t.page_content = clean
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

def process_item(item):
    print(f"Processing item: {item}")
    process_file(item)
    # Add your processing logic here
def process_items(items):
    print(f"Processing item: {items}")
    for i in items:
        process_file(i)


def worker(queue):
    while True:
        item = queue.get()
        if item is None:
            break
        process_item(item)
        queue.task_done()

def main():
    folder_path = sys.argv[1]

    max_threads = 24

    item_queue = []
    total_items = 0
    
    # Add items to the queue
    for root, _, files in os.walk(folder_path):
        for file in files:
            group = []
            file_path = os.path.join(root, file)
            _, file_extension = os.path.splitext(file_path)
            # only do file types we want to process
            if file_extension.lower() in ('.pdf', '.md', '.txt', '.html', '.pptx', '.docx'):
                group.append(file_path)
                total_items= total_items+1
            item_queue.append(group)

    starttime = time.time()
    pool = multiprocessing.Pool(processes=max_threads)
    pool.map(process_items, item_queue)
    pool.close()
    print('That took {} seconds'.format(time.time() - starttime))
    print(f"processing a total of {total_items} of files" )
if __name__ == "__main__":
    main()
