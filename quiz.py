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
