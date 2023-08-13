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
        json_request = request.json
        if json_request is None:
            return "Bad Request", 400
        
        log_request(json_request)
        bot.route_message(json_request)
        return "OK", 200

    if request.method == "GET":
        hub_verify_token = request.args.get('hub.verify_token')
        if str(hub_verify_token) != os.getenv("WHATSAPP_CALLBACK_VERIFY_TOKEN"):
            return "Bad Verify Code", 401 
        
        hub_challenge = request.args.get('hub.challenge') # Required to return this for webhook setup
        if hub_challenge is None:
            return "Bad Request", 400
            
        return hub_challenge, 200

if __name__ == '__main__':
    app.run()
