import random

class Quiz:
    def __init__(self, table_client):
        self.table_client = table_client

    def get_random_word(self):
        entities = list(self.table_client.list_entities())
        if entities:
            random_word = random.choice(entities)
            return {
                'word': random_word['word'],
                'meanings': random_word['meanings'].split(', '),  # Split string back into a list
                'sentences': random_word['sentences'].split(', ')  # Split string back into a list
            }
        else:
            return None

    def check_answer(self, word_id, user_answer):
        # Retrieve the word entry from the Azure Table Storage using word_id (RowKey)
        entity = self.table_client.get_entity(partition_key='vocab', row_key=word_id)
        meanings = entity['meanings'].split(', ')  # Split meanings from the stored format

        # Convert to lowercase for case-insensitive comparison
        user_answer_lower = user_answer.lower()

        # Check if the user's answer is a substring of any of the meanings (case-insensitive)
        for meaning in meanings:
            if user_answer_lower in meaning.lower():
                return True

        return False
