from datetime import datetime


class Logger:
    _DEBUG = False

    @staticmethod
    def set_debug(debug):
        Logger._DEBUG = debug

    @staticmethod
    def log(message, is_debug=True):
        if not is_debug: print(f"[{datetime.now()}] {message}")
        elif Logger._DEBUG: print(f"[{datetime.now()}] {message}")
