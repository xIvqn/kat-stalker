from jobs.job import Job
from logger import Logger
from telegram import Telegram


_telegram = Telegram()

class Scores(Job):

    @staticmethod
    def do(chat_id, previous, current):
        Logger.log(f"Executing Scores job for affiliation {current['name']}")
        updates = {
            'new': [],
            'win': [],
            'lose': [],
        }
        for user_current in current['users']:
            user_previous = Scores._get_user_data(user_current['nickname'], previous)
            if not user_previous:
                updates['new'].append({
                    'current': user_current,
                    'affiliation': current['name'],
                })
            else:
                update = {
                    'previous': user_previous,
                    'current': user_current,
                }
                if user_previous['score'] > user_current['score']:
                    updates['win'].append(update)
                elif user_previous['score'] < user_current['score']:
                    updates['lose'].append(update)

        Logger.log(f"Obtained: {len(updates['new'])} new users, {len(updates['win'])} wins, {len(updates['lose'])} loses.")
        Logger.log("Sending updates to telegram chat.")
        for update_type, updates_ in updates.items():
            for update in updates_:
                _telegram.send(chat_id, Scores._get_message(update, update_type))

    @staticmethod
    def _get_user_data(nickname, affiliation):
        if not affiliation: return None
        if len(affiliation) == 0: return None
        if not affiliation['users']: return None

        for user in affiliation['users']:
            if user['nickname'] == nickname: return user

        return None

    @staticmethod
    def _get_message(update, msg_type):
        name = f"{update['current']['user']} \( [{update['current']['nickname']}](https://open.kattis.com/users/{update['current']['nickname']}) \)"
        if msg_type == 'new':
            return f"✅ {name} se ha inscrito en el [ranking](https://open.kattis.com/affiliation/{update['affiliation']}) con una puntuación de {update['current']['score']} puntos."
        elif msg_type == 'win' or msg_type == 'lose':
            return f"‼️ {name} ha {'ganado' if msg_type == 'win' else 'perdido'} {abs(update['current']['score'] - update['previous']['score'])} puntos.\n\nPosición actual: {'↗️ ' if update['current']['rank'] > update['previous']['rank'] else '↗↘️ ' if update['current']['rank'] > update['previous']['rank'] else ''} {update['current']['rank']} ({update['current']['score']} puntos)."