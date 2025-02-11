import sys

import parser
from jobs.job import Job
from logger import Logger
from telegram import Telegram


_telegram = Telegram()

class Scores(Job):

    @staticmethod
    def do(chat_id, previous, current):
        args = parser.parse_args()

        Logger.log(f"Executing Scores job for affiliation {current['name']}")
        updates = Scores.build_updates(args.join_msg, args.lose_score, args.threshold, current, previous)

        Logger.log(f"Obtained: {len(updates['new'])} new users, {len(updates['win'])} wins, {len(updates['lose'])} loses.")
        Logger.log(f"Sending updates to telegram chat as {'summary' if args.summary else 'individual'}.")
        if args.summary: Scores.send_summary_message(chat_id, updates)
        else: Scores.send_individual_messages(chat_id, updates)

    @staticmethod
    def send_individual_messages(chat_id, updates):
        for update_type, updates_ in updates.items():
            for update in updates_:
                try:
                    _telegram.send(chat_id, Scores._get_individual_message(update, update_type))
                except Exception as e:
                    print(f"Failed to send update from {update['current']['nickname']}: {e}", file=sys.stderr)

    @staticmethod
    def send_summary_message(chat_id, updates):
        try:
            message = Scores._get_summary_message(updates)
            if message: _telegram.send(chat_id, message)
        except Exception as e:
            print(f"Failed to send summary to {chat_id}: {e}", file=sys.stderr)

    @staticmethod
    def build_updates(join_msg, lose_score, threshold, current, previous):
        updates = {
            'new': [],
            'win': [],
            'lose': [],
        }
        for user_current in current['users']:
            user_previous = Scores._get_user_data(user_current['nickname'], previous)
            if not user_previous:
                if join_msg:
                    updates['new'].append({
                        'current': user_current,
                        'affiliation': current['name'],
                    })
            else:
                update = {
                    'previous': user_previous,
                    'current': user_current,
                }
                if abs(user_previous['score'] - user_current['score']) < threshold:
                    continue
                elif user_previous['score'] < user_current['score']:
                    updates['win'].append(update)
                elif user_previous['score'] > user_current['score']:
                    if lose_score: updates['lose'].append(update)
        return updates

    @staticmethod
    def _get_user_data(nickname, affiliation):
        if not affiliation: return None
        if len(affiliation) == 0: return None
        if not affiliation['users']: return None

        for user in affiliation['users']:
            if user['nickname'] == nickname: return user

        return None

    @staticmethod
    def _get_individual_message(update, msg_type):
        name = f"{update['current']['user']} \( [{update['current']['nickname']}](https://open.kattis.com/users/{update['current']['nickname']}) \)"
        if msg_type == 'new':
            return f"✅ {name} se ha inscrito en el [ranking](https://open.kattis.com/affiliation/{update['affiliation']}) con una puntuación de {update['current']['score']} puntos."
        elif msg_type == 'win' or msg_type == 'lose':
            return f"{'🤩' if msg_type == 'win' else '🙁'} {name} ha {'ganado' if msg_type == 'win' else 'perdido'} {round(abs(update['current']['score'] - update['previous']['score']), 2)} puntos\!\n\nPosición actual: {'⬆️ ' if update['current']['rank'] > update['previous']['rank'] else '⬇️ ' if update['current']['rank'] > update['previous']['rank'] else ''}{update['current']['rank']} \({update['current']['score']} puntos\)."

    @staticmethod
    def _get_summary_message(updates):
        message = []
        for update_type in updates.keys():
            if not updates[update_type]: continue

            msg = [Scores._get_individual_message(update, update_type).replace('\n\n', ' ') for update in updates[update_type]]
            message.append(
                f"Nuevos usuarios {'se han unido a la clasificación' if update_type=='new' else 'han ganado puntos' if update_type=='win' else 'han perdido puntos' if update_type=='lose' else ''}:\n\n" \
                + "\n".join(msg)
            )
        return "\n\n\n".join(message)