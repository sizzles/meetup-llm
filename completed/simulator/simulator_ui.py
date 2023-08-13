import streamlit as st
import requests
from flask import Flask, request
from threading import Thread
#Simulator Url

simulator_port = 6000
simulator_server = f"http://localhost:{simulator_port}"
llm_server = "http://localhost:5000"


# Streamlit app
st.title("WhatsApp Message Simulator")

# Phone numbers
phone_numbers = st.sidebar.text_area("Enter phone numbers (one per line):").split('\n')

# Select a phone number
selected_phone_number = st.sidebar.selectbox("Select a phone number:", phone_numbers)

# Retrieve chat for the selected phone number from the Flask app
response = requests.get(f"{simulator_server}/get_chat?wa_id={selected_phone_number}")
current_chat = response.json().get('chat', [])

# Display chat
for message in current_chat:
    if message['from'] == 'user':
        st.write(f"{selected_phone_number}: {message['text']}")
    else:
        st.write(f"AI: {message['text']}")

# Send a message
user_message = st.text_input("Enter your message:")
if st.button("Send"):
    # Message body to be sent to the Flask app
    message_body = {
        'object': 'whatsapp_business_account',
        'entry': [{
            'id': '12345',
            'changes': [{
                'value': {
                    'messaging_product': 'whatsapp',
                    'metadata': {
                        'display_phone_number': '12345',
                        'phone_number_id': '12345'
                    },
                    'contacts': [{'profile': {'name': 'Simulator'}, 'wa_id': selected_phone_number}],
                    'messages': [{'from': selected_phone_number, 'id': 'message_id', 'timestamp': 'timestamp', 'text': {'body': user_message}, 'type': 'text'}]
                },
                'field': 'messages'
            }]
        }]
    }

    # Send the message to the Flask app
    response = requests.post(f"{simulator_server}/send", json=message_body)

    if response.status_code == 200:
        st.success("Message sent.")
    else:
        st.error("Failed to send message.")

st.button('Reload')