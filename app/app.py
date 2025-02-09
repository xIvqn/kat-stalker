import argparse
import os

import parser
from db import KatStalkerDb
from jobs.factory import JobFactory
from logger import Logger
from scrapper import Scrapper

class App:
    def __init__(self):
        self.database = KatStalkerDb()
        self.args = parser.parse_args()
        self.jobs = JobFactory.get_all(self.args.jobs)
        Logger.set_debug(self.args.debug)
        Logger.log(f"Setting debug mode to {self.args.debug}")

    def run(self):
        Logger.log("Starting app", is_debug=False)

        chats = self.database.get_chats()
        for i, chat in enumerate(chats):
            self._process_chat(chat, i)

        Logger.log("Finished processing chats", is_debug=False)


    def _process_chat(self, chat, index):
        if chat['chat_id'] == "":
            Logger.log(f"Skipping chat {index}", is_debug=False)
            return

        Logger.log(f"Processing chat {index}", is_debug=False)
        affiliations = [Scrapper.scrape_affiliation(affiliation['url']) for affiliation in chat['affiliations']]
        for affiliation in affiliations:
            for job in self.jobs:
                job.do(chat['chat_id'], self.database.get_affiliation(chat['chat_id'], affiliation['name']), affiliation)
        self.database.save_chat(chat['chat_id'], affiliations)
