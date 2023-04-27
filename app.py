from flask import Flask, render_template, request, redirect, url_for
import os
import time
import re
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import DirectoryLoader
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain

embeddings = OpenAIEmbeddings(openai_api_key=os.environ['OPENAI_API_KEY'])
app = Flask(__name__)

UPLOAD_FOLDER = 'uploaded_files'
ALLOWED_EXTENSIONS = {'pdf'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
directory_path = './'
files_and_directories = os.listdir(directory_path)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_sample_names():
    folders = []
    for item in files_and_directories:
    # check if the item is a directory and ends with "_faiss"
        if os.path.isdir(os.path.join(directory_path, item)) and item.endswith('_faiss'):
            folders.append(item[:-6])
    return folders

@app.route('/')
def index():
    sample_names = get_sample_names()
    return render_template('index.html', sample_names=sample_names)


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        folder_name = request.form['folder_name']
        file = request.files['file']

        if file and allowed_file(file.filename):
            folder_path = os.path.join(app.config['UPLOAD_FOLDER'], folder_name)
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)

            file_path = os.path.join(folder_path, file.filename)
            file.save(file_path)
            return redirect(url_for('index'))

    return render_template('upload.html')


@app.route('/train', methods=['GET', 'POST'])
def train():
    if request.method == 'POST':
        # Add your training logic here
        index = request.form['input_text']
        pdf_folder_path = f'{UPLOAD_FOLDER}/{index}/'
        loader = DirectoryLoader("{}".format(pdf_folder_path))
        data = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        texts = text_splitter.split_documents(data)
        faiss_index_name = "{}_faiss".format(index)
        docsearch = FAISS.from_texts([t.page_content for t in texts], embeddings, index_name=faiss_index_name)
        docsearch.save_local(faiss_index_name)
        return redirect(url_for('success'))
    return render_template('train.html')


@app.route('/success', methods=['GET', 'POST'])
def success():
    search_results = None
    if request.method == 'POST':
        query = request.form['query']
        # query = query + 'Try to find the answer in data provided. In you dont know the answer then simply say i couldnt find any relevent response.'
        index_name = request.form['index_name']
        search_type = request.form['type']
        search_results = perform_search(query, index_name, search_type)
    sample_names = get_sample_names()
    return render_template('success.html', search_results=search_results, sample_names=sample_names)



def perform_search(query, index_name, search_type):
    # Implement your search logic here
    # For now, we will return a sample result list
    index = index_name
    faiss_index_name = "{}_faiss".format(index)
    docsearch = FAISS.load_local(faiss_index_name, embeddings)
    llm = OpenAI(temperature=0, openai_api_key=OPENAI_API_KEY)
    chain = load_qa_chain(llm, chain_type="stuff", verbose = False)
    if search_type == 'text':
        docs = docsearch.similarity_search(query)
    elif search_type == 'image':
        docs = docsearch.similarity_search(query + 'Image')
    docs = docsearch.similarity_search(query)
    answer = chain.run(input_documents=docs, question=query)
    return [answer]

def urlize(text):
    url_pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    return url_pattern.sub(lambda match: f'<a href="{match.group(0)}" target="_blank">{match.group(0)}</a>', text)


app.jinja_env.filters['urlize'] = urlize

if __name__ == '__main__':
    app.run(debug=False, host = '0.0.0.0')
