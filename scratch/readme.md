WhatsApp Cake Ordering System 'Snake Cakes' - Requirements Document

Introduction:
This project involves building an interactive WhatsApp bot for a cake-selling company. Its role is to facilitate the placement of orders, hold conversations, and generate orders in the internal system, all while potentially upselling related products.

Functional Requirements:

app.py (Flask Web Server)

Establish a Flask-based application.
Incorporate logging to capture activities, errors, and significant events.
Handle incoming requests, manage verification, and route messages to the bot.
bot/bot.py (Core Bot Logic)

Initiate core services like WhatsApp interaction, chat sessions, message caching, and routing.
Employ threading to manage incoming message queues efficiently and be able to handle multiple requests.
Use locks to ensure thread safety, particularly when dealing with shared resources.
It is imperative to respond to the incoming WhatsApp cloud webhook with 250 milliseconds, before exponentially
backed of retries start being sent to you!

bot/chat

Develop a chat repository to oversee individual chat sessions with users.
Enable the continuation of existing chats or the initiation of new ones.
Preserve chat sessions for consistent interactions across sessions.
You can use json and a local file system for an easy way to get started.

bot/llms

Integrate a language learning model using the OpenAI GPT AI, to process and formulate responses.
Ensure the model can interpret a variety of user queries, spanning order placements to product queries.

bot/prompts

Construct predefined templates or responses for frequent interactions.
Develop a system to manage and retrieve these templates for consistent responses.

bot/routing

Design a system to route incoming messages to the correct handlers or services.
Ensure efficient message routing, especially during high traffic times.

bot/whatsapp

Interface with the WhatsApp API for message sending.
Implement queue based logic.

bot/msg_cache

Design a caching mechanism to temporarily store recent messages or session data.
This is because users often send multiple messages quickly after one another.
This allows you to check you are processing the latest before sending a reply.

configuration

Come up with a method for managing keys and configuration. For example, env files.


Non-Functional Requirements:

Performance

Design for swift response times and efficient message processing.

Reliability
Build robust error handling mechanisms and think about retries.

Development Milestones:

Setup: Initialize Flask, bot, and logging.
Core Development: Develop bot logic, chat management, and LLM integration.
Integration: Interface with WhatsApp and verify message interactions.