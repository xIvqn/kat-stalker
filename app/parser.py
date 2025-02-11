import argparse

from jobs import scores
from logger import Logger


_args = None

def parse_args():
    global _args

    Logger.log('Parsing arguments')
    parser = argparse.ArgumentParser(description="Process jobs with various options.")

    parser.add_argument("-j", "--jobs", nargs="+", help="List of job names")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug mode")
    parser.add_argument("-s", "--summary", action="store_true", help="Enable summary mode")
    parser.add_argument("--lose-score", action="store_true", help="Send lose score messages")
    parser.add_argument("--join-msg", action="store_true", help="Send join messages")
    parser.add_argument("-t", "--threshold", type=float, default=1.0, help="Threshold for score messages. If change is lower than this, score updates will not be sent.")

    _args = parser.parse_args()

    Logger.log(f'Parsed: {_args}', is_debug=True)

    return _args

def get_args():
    return _args
