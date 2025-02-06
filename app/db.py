import os

from bson import ObjectId
from pymongo import MongoClient

from logger import Logger


class KatStalkerDb:
    def __init__(self):
        Logger.log('Establishing connection to MongoDB')
        self.client = MongoClient(os.getenv('DATABASE_URI', 'mongodb+srv://user:pass@localhost:27017'),)
        self.db = self.client[os.getenv('DATABASE_NAME', 'katstalker')]
        Logger.log('Successfully connected to DB')

    def close(self):
        self.client.close()

    def get_chats(self):
        return self.db['chats'].find({})

    def get_affiliations(self, chat_id):
        return self.db['chats'].find_one({'chat_id': chat_id})['affiliations']

    def get_affiliation(self, chat_id, name):
        for affiliation in self.get_affiliations(chat_id):
            if affiliation['name'] == name: return affiliation

    def save_chat(self, chat_id, affiliations):
        Logger.log('Saving affiliation data in DB')
        self.db["chats"].update_one(
            {'chat_id': chat_id},
            {'$set': {
                'affiliations': affiliations
            }}
        )

