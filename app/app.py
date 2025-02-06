import os

from db import KatStalkerDb
from jobs.factory import JobFactory
from logger import Logger
from scrapper import Scrapper

class App:
    def __init__(self):
        self.database = KatStalkerDb()
        self.jobs = JobFactory.get_all(os.getenv('JOBS', "").split(";"))

    def run(self, debug=False):
        Logger.log("Starting app", is_debug=False)
        Logger.set_debug(debug)
        Logger.log(f"Setting debug mode to {debug}")

        chats = self.database.get_chats()
        for i, chat in enumerate(chats):
            self._process_chat(chat, i)

        Logger.log("Finished processing chats", is_debug=False)


    def _process_chat(self, chat, index):
        Logger.log(f"Processing chat {index}", is_debug=False)
        affiliations = [Scrapper.scrape_affiliation(affiliation['url']) for affiliation in chat['affiliations']]
        for affiliation in affiliations:
            for job in self.jobs:
                job.do(chat['chat_id'], self.database.get_affiliation(chat['chat_id'], affiliation['name']), affiliation)
        self.database.save_chat(chat['chat_id'], affiliations)
