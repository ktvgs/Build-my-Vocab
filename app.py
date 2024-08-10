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

# Create a TableServiceClient
table_service = TableServiceClient.from_connection_string(conn_str=connection_string)
table_client = table_service.get_table_client(table_name)

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
        'meanings': ', '.join(data['meaning']),
        'sentences': ', '.join(data['sentence'])
    }

    # Insert the entity into the table
    table_client.create_entity(entity=word_entry)
    
    return jsonify({"message": "Word added successfully!"}), 201

@app.route('/get_random_word', methods=['GET'])
def get_random_word():
    random_word = quiz.get_random_word()
    if random_word:
        return jsonify(random_word)
    else:
        return jsonify({"message": "No words found in the database"}), 404

if __name__ == '__main__':
    app.run(debug=True)
