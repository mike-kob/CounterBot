import os


TOKEN = os.environ.get('BOT_TOKEN')
APP_NAME = os.environ.get("APP_NAME")
AUTH_STRING = os.environ.get("AUTH_STRING")

class STATUS:
    home = 0
    add_counter = 1
    count = 2
