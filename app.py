import os
from flask import Flask, request, redirect, url_for, flash, render_template, jsonify, make_response
from werkzeug.utils import secure_filename
from langchain.document_loaders import PyPDFLoader
from embeddings import query_index

import tenacity

app = Flask(__name__, static_folder='static')
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "super_secret_key")
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['CONVERTED_FOLDER'] = 'converted_files'

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


def allowed_file(filename):
  return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'pdf'






@app.route('/', methods=['GET'])
def index():
  return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'pdf_file' not in request.files:
        flash('No file part')
        return redirect(url_for('index'))

    file = request.files['pdf_file']

    if file.filename == '':
        flash('No file selected')
        return redirect(url_for('index'))

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # Load and split PDF using LangChain's PyPDFLoader
        loader = PyPDFLoader(file_path)
        pages = loader.load_and_split()

        # Combine pages into one string
        text_content = '\n'.join([page.page_content for page in pages])

        txt_filename = os.path.splitext(filename)[0] + '.txt'
        txt_file_path = os.path.join(app.config['CONVERTED_FOLDER'], txt_filename)
        with open(txt_file_path, 'w') as txt_file:
            txt_file.write(text_content)

        flash('File uploaded and converted successfully')
        return redirect(url_for('index'))
    else:
        flash('Invalid file format')
        return redirect(url_for('index'))



@app.route("/send_message", methods=["POST"])
def send_message():
  query = request.form["user_message"]
  logging.info(query)
  n_results = 5  # You can change this to any number you prefer
  index_name = "pwc-risk"  # Replace this with your index name
  results = query_index(query, n_results, index_name)
  logging.info(results)
  return jsonify({"message": query})
  
 
#
  #@tenacity.retry(stop=tenacity.stop_after_attempt(5),
  #              wait=tenacity.wait_exponential(multiplier=1, min=2, max=30),
  #              retry=tenacity.retry_if_exception_type(ConnectionResetError),
  #              reraise=True)
  #def make_request_with_retry():
  #  results = query_index(query, n_results, index_name)
  #  return jsonify(results)
#
  #return make_request_with_retry()
  



if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8080)
