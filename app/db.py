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

    def get_affiliations(self):
        return self.db['affiliations'].find({})

    def get_affiliation(self, name):
        return self.db['affiliations'].find_one({'name': name})


    def _insert_affiliation(self, affiliation):
        self.db["affiliations"].insert_one(affiliation)

    def _update_affiliation(self, affiliation):
        self.db["affiliations"].update_one(
            {'name': affiliation['name']},
            {'$set': affiliation}
        )

    def save_affiliation(self, affiliation):
        Logger.log('Saving affiliation data in DB')
        db_affiliation = self.get_affiliation(affiliation['name'])
        if db_affiliation is None: self._insert_affiliation(affiliation)
        else: self._update_affiliation(affiliation)

