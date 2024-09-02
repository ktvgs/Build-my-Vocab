from flask import Flask, request, jsonify, send_from_directory
from azure.data.tables import TableServiceClient
import os
import uuid
from dotenv import load_dotenv
from quiz import Quiz  # Importing the quiz logic

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Fetch connection string from environment variables
connection_string = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
table_name = 'VocabTable'

# Define a client for the vocabAnalyzer table
analyzer_table_name = 'vocabAnalyzer'



# Create a TableServiceClient
table_service = TableServiceClient.from_connection_string(conn_str=connection_string)
table_client = table_service.get_table_client(table_name)

analyzer_table_client = table_service.get_table_client(analyzer_table_name)

# Initialize Quiz with the TableServiceClient
quiz = Quiz(table_client)

@app.route('/')
def serve_home():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('.', path)

@app.route('/add_word', methods=['POST'])
def add_word():
    data = request.get_json()
    word_entry = {
        'PartitionKey': 'vocab',
        'RowKey': str(uuid.uuid4()),  # Unique identifier for each entry
        'word': data['word'],
        'meanings': data['meaning'],
        'sentences': data['sentence']
    }

    # Insert the entity into the table
    table_client.create_entity(entity=word_entry)
    
    return jsonify({"message": "Word added successfully!"}), 201

@app.route('/check_answer', methods=['POST'])
def check_answer():
    data = request.get_json()
    word_id = data['word_id']
    user_answer = data['answer']

    if quiz.check_answer(word_id, user_answer):
        return jsonify({"message": "Correct!"}), 200
    else:
        return jsonify({"message": "Incorrect, try again!"}), 200

@app.route('/vocab_stats', methods=['GET'])
def get_vocab_stats():
    # Get all records from the vocabAnalyzer table
    entities = analyzer_table_client.list_entities()
    
    # Initialize counters
    total_words_used = 0
    total_documents = 0

    for entity in entities:
        total_words_used += int(entity['num_words_used'])
        total_documents += 1
    
    return jsonify({
        "total_words_used": total_words_used,
        "total_documents": total_documents
    }), 200


if __name__ == '__main__':
    app.run(debug=True)
