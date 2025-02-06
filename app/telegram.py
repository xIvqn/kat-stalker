import os
from html import escape

import requests


class Telegram:
    def __init__(self):
        self.token = os.environ['TELEGRAM_TOKEN']

    def send(self, chat_id, message):
        message = escape(message).replace('.', '\\.').replace('-', '\\-')
        url = f'https://api.telegram.org/bot{self.token}/sendMessage?chat_id={chat_id}&text={message}&parse_mode=MarkdownV2'
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception('Telegram Error - could not send message: {}'.format(response.text))
