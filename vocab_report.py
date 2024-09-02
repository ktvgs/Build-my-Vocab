import os
import re
from azure.data.tables import TableServiceClient
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Fetch connection string from environment variables
connection_string = os.getenv('AZURE_STORAGE_CONNECTION_STRING')

# Initialize table clients
vocab_table_name = 'VocabTable'
analyzer_table_name = 'vocabAnalyzer'
table_service = TableServiceClient.from_connection_string(conn_str=connection_string)
vocab_table_client = table_service.get_table_client(vocab_table_name)
analyzer_table_client = table_service.get_table_client(analyzer_table_name)

# Function to fetch words from Azure Table Storage
def fetch_words_from_table():
    words = set()
    entities = vocab_table_client.list_entities()
    for entity in entities:
        words.add(entity['word'].lower())
    return words

# Function to count occurrences of words in a file
def count_word_occurrences(file_path, vocab_words):
    word_count = {word: 0 for word in vocab_words}
    with open(file_path, 'r') as file:
        text = file.read().lower()
        for word in vocab_words:
            word_count[word] = len(re.findall(r'\b' + re.escape(word) + r'\b', text))
    return word_count

# Function to get the list of processed files
def get_processed_files(processed_files_path):
    if os.path.exists(processed_files_path):
        with open(processed_files_path, 'r') as file:
            return set(line.strip() for line in file)
    return set()

# Function to add a file to the processed list
def mark_file_as_processed(processed_files_path, filename):
    with open(processed_files_path, 'a') as file:
        file.write(filename + '\n')

# Function to store word usage data in the vocabAnalyzer table
def store_word_usage_data(file_name, word_counts):
    used_words = [word for word, count in word_counts.items() if count > 0]
    num_words_used = len(used_words)
    
    entity = {
        'PartitionKey': 'document_id',
        'RowKey': file_name,
        'num_words_used': num_words_used,
        'words_list': ', '.join(used_words)
    }
    
    analyzer_table_client.create_entity(entity)

def process_new_files(directory, processed_files_path):
    vocab_words = fetch_words_from_table()
    processed_files = get_processed_files(processed_files_path)
    
    for filename in os.listdir(directory):
        if filename.endswith(".txt") and filename not in processed_files:
            file_path = os.path.join(directory, filename)
            print(f"Processing new file: {file_path}")
            
            word_counts = count_word_occurrences(file_path, vocab_words)
            print(f"Word counts for {filename}: {word_counts}")
            
            # Store data in the vocabAnalyzer table
            store_word_usage_data(filename, word_counts)
            
            mark_file_as_processed(processed_files_path, filename)

if __name__ == "__main__":
    blogs_directory = "./blogs"  # Path to the blogs folder
    processed_files_path = "./processed_files.txt"  # Path to the file tracking processed files
    process_new_files(blogs_directory, processed_files_path)
