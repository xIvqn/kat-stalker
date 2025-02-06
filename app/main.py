import os

from app import App

if __name__ == '__main__':
    App().run(debug=os.environ.get('DEBUG', False))
