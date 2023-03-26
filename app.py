import os
from flask import Flask, request, redirect, url_for, flash, render_template, jsonify, make_response
from werkzeug.utils import secure_filename
from langchain.document_loaders import PyPDFLoader
from embeddings import query_index, embed_document
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import ChatPromptTemplate, HumanMessagePromptTemplate
from pymongo import MongoClient
from dotenv import load_dotenv
from bson.binary import Binary
import io

load_dotenv()




app = Flask(__name__, static_folder='static')
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "super_secret_key")


mongo_username = os.environ.get("MONGO_USERNAME")
mongo_password = os.environ.get("MONGO_PASSWORD")
mongo_cluster_address = os.environ.get("MONGO_CLUSTER_ADDRESS")
mongo_db_name = os.environ.get("MONGO_DB_NAME")
MONGO_URI = f"mongodb+srv://{mongo_username}:{mongo_password}@{mongo_cluster_address}/{mongo_db_name}?retryWrites=true&w=majority"
client = MongoClient(MONGO_URI)
db = client.get_database(mongo_db_name)
file_collection = db['files']


NUMBER_RESULTS = 5
INDEX_NAME = 'pwc-risk'

import logging
import sys

logging.basicConfig(
  level=logging.DEBUG,
  format='%(asctime)s [%(levelname)s] %(message)s',
  handlers=[
      logging.FileHandler("console_output.txt", mode='w'),
      logging.StreamHandler(sys.stdout)
  ]
)


# Initialize LLM
llm = ChatOpenAI(temperature=0.9)

# Set up the initial prompt template
initial_qa_template = (
    "Context information is below. \n"
    "---------------------\n"
    "{context_str}"
    "\n---------------------\n"
    "Given the context information and not prior knowledge, "
    "answer the question: {question}"
)
initial_qa_prompt = PromptTemplate(input_variables=["context_str", "question"], template=initial_qa_template)

# Set up the LLMChain
human_message_prompt = HumanMessagePromptTemplate(prompt=initial_qa_prompt)
chat_prompt_template = ChatPromptTemplate.from_messages([human_message_prompt])
chain = LLMChain(llm=llm, prompt=chat_prompt_template)

def allowed_file(filename):
  return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'pdf'

@app.route('/', methods=['GET'])
def index():
  return render_template('index.html')

import os
import tempfile

@app.route('/upload', methods=['POST'])
def upload_file():
    logging.info("Upload request received.")
    if 'pdf_file' not in request.files:
        flash('No file part')
        return redirect(url_for('index'))

    file = request.files['pdf_file']

    if file.filename == '':
        flash('No file selected')
        return redirect(url_for('index'))

    if file and allowed_file(file.filename):
        logging.info(f"Processing file: {file.filename}")
        filename = secure_filename(file.filename)

        # Save the file temporarily
        temp_dir = tempfile.mkdtemp()
        temp_path = os.path.join(temp_dir, filename)
        file.save(temp_path)

        # Load and split PDF using LangChain's PyPDFLoader
        loader = PyPDFLoader(file_path=temp_path)
        pages = loader.load_and_split()

        # Combine pages into one string
        text_content = '\n'.join([page.page_content for page in pages])

        # Embed and upload the document to Pinecone
        index_name = INDEX_NAME
        embed_document(filename, text_content, index_name)

        # Insert file and its text content into MongoDB
        file_document = {
            'filename': filename,
            'content': text_content,
            'pdf_file': pdf_binary
        }
        file_collection.insert_one(file_document)

        # Remove the temporary file and directory
        os.remove(temp_path)
        os.rmdir(temp_dir)

        flash('File uploaded, converted, and embedded successfully')
        return redirect(url_for('index'))
    else:
        flash('Invalid file format')
        return redirect(url_for('index'))

@app.route("/send_message", methods=["POST"])
def send_message():
  user_message = request.form["user_message"]
  n_results = 5  
  index_name = "pwc-risk"  # Replace this with your index name

  if user_message:
    query = user_message
    query_result = query_index(query, n_results, index_name)
    context_str = "\n\n".join([doc["page_content"] for doc in query_result.values()])
    response = chain.run({"context_str": context_str, "question": query})
    
    return jsonify({"message": query_result, "answer": response})
  else:
    return jsonify({"message": "No message provided"})





if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8080)
