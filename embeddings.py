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


#loader = TextLoader('./converted_files/PTR_Guidance_Note_1.txt')

#documents = loader.load()
#text_splitter = CharacterTextSplitter(separator = "\n", chunk_size=1000, #chunk_overlap=0)
#docs = text_splitter.split_documents(documents)
#embeddings = OpenAIEmbeddings()



# initialize pinecone
#pinecone.init(
#    api_key=os.environ["PINECONE_API_KEY"],  # find at app.pinecone.io
#    environment=os.environ["PINECONE_ENVIRONMENT"]  # next to api key in console
#)

#index_name = "hackathon-test"

#docsearch = Pinecone.from_documents(docs, embeddings, index_name=index_name)

#query = "How often does an entity need to report their income?"
#docs = docsearch.similarity_search(query)

#print(docs[0].page_content)

def embed_document(filename, text_content, index_name):
    print(f"Embedding document: {filename}")
    
    text_splitter = CharacterTextSplitter(separator="\n", chunk_size=1000, chunk_overlap=100)
    docs = text_splitter.split(text_content)
    
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
  #print(docs[0].page_content)
  #logging.info(docs[0].page_content)

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

#embed_document('./converted_files/2021-alp-national-platform-final-endorsed-platform.txt', 'pwc-risk')

#query_index("What will Labor do about Climate Change?", 5, "pwc-risk")