import queue
from .prompts import PromptService, Prompt
import queue
import threading
import concurrent.futures
import datetime as dt
import logging
import os
import traceback
from .chat import Chat, ChatRepository
from .llms import GPTLLM, Model, LLMResponse
from .whatsapp import WhatsAppService
from .msg_cache import MsgCache
from .routing import RoutingService

class Bot:
    def __init__(self) -> None:
        self.whatsapp_service = WhatsAppService()
        self.chat_repository = ChatRepository(str(os.getenv("DATA_FOLDER")))
        self.whatsapp_admin_number = os.getenv("WHATSAPP_ADMIN_NUMBER")
        self.msg_cache = MsgCache()
        self.incoming_msg_q = queue.Queue()
        self.routing_service = RoutingService(self.incoming_msg_q, self.msg_cache)
        self.queue_processor()

    def queue_processor(self):
        logging.info("Creating Incoming Queue Processors.")
        incoming_workers = 1
        incoming_executor = concurrent.futures.ThreadPoolExecutor(
            max_workers=incoming_workers, thread_name_prefix="incoming"
        )
        for _ in range(incoming_workers):
            incoming_executor.submit(self.incoming_worker_task)
        logging.info("Created Incoming Queue Processors.")

    def incoming_worker_task(self):

        prompt_service = PromptService(os.getenv("PROMPT_DIRECTORY"))

        while True:
            try:
                """TODO - processing steps for the main bot loop
                1) Extract the wa_id (telephone number) from the incoming message queue using get.
                2) Load messages from the current cached messages for this wa_id
                3) Check if the user already has a chat saved to disk
                4) *OPTIONAL* Call the is_valid method on a chat loaded from disk to see if we should process.
                    If not just on continue in the loop. For example too much has already been spent on this user
                5) If we have a new user, create an initial prompt and input their message 
                6) If it was an existing user, create a continuation prompt and input their message
                7) Create an instance of the GPTLLM model class
                8) Get the initial repsonse to the cutomer query 
                9) Create a CUS response prompt + set the model mode to gpt 3.5
                10) Get a response for the CUS prompt, which contain only the text we need to send back to the user.
                11) *OPTIONAL* use caching and locking to control access to the message cache. If using a thread worker count of 1, not needed.
                12) Save the updated chat history for the user - using the original LLM response
                13) Send a response back to the user with the CUS reponse message
                
                Implemented code is below - delete this and follow the steps above.

                """

                

                wa_id = self.incoming_msg_q.get()
                logging.info(f"Processing message for: {wa_id}")

                input_message, last_received = self.msg_cache.get_cached_msgs(wa_id)

                if input_message is None:
                    continue  # Handling race conditions of another thread picking up our messages

                # Do we have an existing conversation?
                chat = self.chat_repository.load_chat(wa_id)

                if chat is not None:
                    # check if the chat is valid at all
                    chat_valid, valid_msg = chat.is_valid()
                    if not chat_valid:
                        logging.info(f"Chat is not valid - continuing: {wa_id}")
                        self.whatsapp_service.send_message(wa_id, valid_msg)
                        continue

                    prompt: str = (
                        Prompt.build_from(chat.chat_message)
                        .concat(prompt_service.get_continuation_prompt())
                        .to_str({"input_message": input_message})
                    )

                # Build the latest prompt to send to LLM
                else:
                    chat = Chat(wa_id, "", 0)
                    prompt: str = prompt_service.get_initial_prompt().to_str(
                        {
                            "input_message": input_message,
                            "today": dt.datetime.now().strftime("%Y-%m-%d"),
                        }
                    )

                # Build response from saved convo + customers new input message
                gpt_llm = GPTLLM(Model.GPT4, os.getenv("OPENAI_API_KEY"))
                llm_response: LLMResponse = gpt_llm.get_response(prompt)

                # Build repsonse to send to the customer - use gpt 3.5
                gpt_llm.set_model(Model.GPT35)
                cus_response_prompt = prompt_service.get_cus_response_prompt().to_str(
                    {"llm_response": llm_response.response}
                )
                cus_response: LLMResponse = gpt_llm.get_response(cus_response_prompt)

                chat.chat_message = llm_response.concat_response
                chat.cost += (
                    llm_response.cost
                    + cus_response.cost
                )
                chat.has_ended = chat.should_end()
                self.chat_repository.save_chat(chat)

                self.whatsapp_service.send_message(wa_id, cus_response.response)


            except Exception as e:
                logging.exception("Error!")
                logging.exception(e)
                logging.exception(traceback.format_exc())

            finally:
                self.incoming_msg_q.task_done()

    def route_message(self, whatsapp_body):
        self.routing_service.route_message(whatsapp_body)
