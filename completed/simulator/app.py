import streamlit as st
import requests
from flask import Flask, request
from threading import Thread

#Simulator Url

simulator_port = 6000
simulator_server = f"http://localhost:{simulator_port}"
llm_server = "http://localhost:5000"

# Flask app
app = Flask(__name__)

# Dictionary to store chats
chats = {}

@app.route('/incoming', methods=['POST'])
def receive_message():
    print('Receiving message')
    incoming_message = request.json
    wa_id = incoming_message['to']
    text_body = incoming_message['text']['body']

    # Append the incoming message to the corresponding chat
    chat = chats.get(wa_id, [])
    chat.append({'from': 'server', 'text': text_body})
    chats[wa_id] = chat

    return "OK", 200

@app.route('/send', methods=['POST'])
def send_message():
    print('Sending message')
    outgoing_message = request.json
    wa_id = outgoing_message['entry'][0]['changes'][0]['value']['contacts'][0]['wa_id']
    body = outgoing_message['entry'][0]['changes'][0]['value']['messages'][0]['text']['body']

    # Send the message to the external application (adjust the URL)
    response = requests.post(llm_server, json=outgoing_message)

    # Append the sent message to the corresponding chat
    chat = chats.get(wa_id, [])
    chat.append({'from': 'user', 'text': body})
    chats[wa_id] = chat

    return "OK", 200

@app.route('/get_chat', methods=['GET'])
def get_chat():
    wa_id = request.args.get('wa_id')
    return {'chat': chats.get(wa_id, [])}

def run_flask_app():
    
    app.run(port=simulator_port)
    print('Running Simulator Flask App')

run_flask_app
