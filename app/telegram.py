import os
import sys
from html import escape

import requests


class Telegram:
    def __init__(self):
        self.token = os.environ['TELEGRAM_TOKEN']

    def send(self, chat_id, message):
        if chat_id == "":
            print("Skipped empty chat_id")
            return
        message = escape(message)\
            .replace('.', '\\.')\
            .replace('-', '\\-')\
            .replace('_', '\\_')\
            .replace('*', '\\*')
        url = f'https://api.telegram.org/bot{self.token}/sendMessage?chat_id={chat_id}&text={message}&parse_mode=MarkdownV2'
        response = requests.get(url)
        if response.status_code != 200:
            print('Telegram Error - could not send message: {}\n\n{}'.format(response.text, message), file=sys.stderr)
