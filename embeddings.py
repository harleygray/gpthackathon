from langchain.vectorstores import Pinecone
from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import TextLoader
from langchain.embeddings.openai import OpenAIEmbeddings
import os
import pinecone

import logging
import sys

from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler("console_output.txt", mode='w'),
        logging.StreamHandler(sys.stdout)
    ]
)

class TextWrapper:
    def __init__(self, text, metadata=None):
        self.page_content = text
        self.metadata = metadata or {}


def embed_document(filename, pages_content, index_name):
  print(f"Embedding document: {filename}")

  text_splitter = CharacterTextSplitter(separator="\n", chunk_size=1000, chunk_overlap=100)

  docs = []
  for i, page_content in enumerate(pages_content):
      page_chunks = text_splitter.split_text(page_content)
      for chunk in page_chunks:
          # Prepend the page number and filename at the beginning of each chunk
          chunk_with_info = f"Page {i + 1} of {filename}: {chunk}"
          docs.append(TextWrapper(chunk_with_info))

  embeddings = OpenAIEmbeddings()

  # Initialize pinecone
  pinecone.init(
      api_key=os.environ["PINECONE_API_KEY"],
      environment=os.environ["PINECONE_ENVIRONMENT"]
  )

  docsearch = Pinecone.from_documents(docs, embeddings, index_name=index_name)


def query_index(query, n_results, index_name):
  embeddings = OpenAIEmbeddings()
  pinecone.init(
    api_key=os.environ["PINECONE_API_KEY"],  
    environment=os.environ["PINECONE_ENVIRONMENT"]  
)
  docsearch = Pinecone.from_existing_index(index_name, embeddings)
  docs = docsearch.similarity_search(query, n_results)


  # Only add unique page contents
  filtered_docs = []
  seen_page_contents = set()

  for doc in docs:
      if doc.page_content not in seen_page_contents:
          seen_page_contents.add(doc.page_content)
          filtered_docs.append(doc)

  docs_dict = {
      index: {
          'page_content': doc.page_content,
          'metadata': doc.metadata
      }
      for index, doc in enumerate(filtered_docs)
  }

  return docs_dict
