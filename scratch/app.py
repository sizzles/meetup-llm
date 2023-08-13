from flask import Flask, request
import logging
from logging.handlers import RotatingFileHandler
from bot import Bot
from dotenv import load_dotenv
import os


def configure_logging():
    """
    Configure a rotating log handler with a specified file name, size, and backup count.
    """
    LOG_FILE_NAME = 'bot.log'
    MAX_LOG_FILE_SIZE = 30 * 1024 * 1024 # 30 MB
    BACKUP_COUNT = 3

    log_handler = RotatingFileHandler(LOG_FILE_NAME, maxBytes=MAX_LOG_FILE_SIZE, backupCount=BACKUP_COUNT)
    log_handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.addHandler(log_handler)

def log_request(json_request):
    """
    Log the incoming JSON request to a file.
    :param json_request: JSON object to be logged
    """
    logging.getLogger().info(json_request)

load_dotenv(".env")
configure_logging()
bot = Bot()
app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def webhook():
    """
    Handle incoming POST and GET requests.
    POST: Log the incoming JSON and route the message.
    GET: Validate the verification token and return the challenge.
    """
    if request.method == "POST":
        """TODO: Handle post request from whatsapp - contains the actual message to use."""
        pass
    
    if request.method == "GET":
        """TODO: Handle the whatsapp token verify request code. Think about bad requests logic."""

if __name__ == '__main__':
    app.run()
