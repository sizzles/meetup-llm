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
from .orders import Order

convo_lock = threading.Lock()


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
        logging.info("Created Incomine Queue Processors.")

    def incoming_worker_task(self):
        global convo_lock

        prompt_service = PromptService(os.getenv("PROMPT_DIRECTORY"))

        while True:
            try:
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

                # Build response to send to order processing
                gpt_llm.set_model(Model.GPT4)
                order_response_prompt = prompt_service.get_order_prompt().to_str(
                    {"llm_response": llm_response.response}
                )
                order_response: LLMResponse = gpt_llm.get_response(
                    order_response_prompt
                )

                order: Order = Order.from_response(order_response.response)

                # Now check and save the conversation as needed
                with self.msg_cache.cache_lock:
                    latest_messages = self.msg_cache.incoming_msg_cache[wa_id]
                    if len(latest_messages) == 0:  # Race condition - already replied?
                        continue

                    new_last_received = latest_messages[-1].received_at

                    if new_last_received > last_received:
                        # Another message has been sent from the user whils't waiting for reply
                        # Throw away our status and start again
                        self.incoming_msg_q.put(wa_id)
                        continue
                    else:  # clear out the list
                        self.msg_cache.incoming_msg_cache[wa_id] = list()
                        with convo_lock:
                            # save the user
                            chat.chat_message = llm_response.concat_response
                            chat.cost += (
                                llm_response.cost
                                + cus_response.cost
                                + order_response.cost
                            )
                            chat.has_ended = chat.should_end()
                            self.chat_repository.save_chat(chat)

                        self.whatsapp_service.send_message(wa_id, cus_response.response)

                        # Send order update to admin if needed
                        if order and order.has_order:
                            self.whatsapp_service.send_message(
                                self.whatsapp_admin_number, order.order_details
                            )

            except Exception as e:
                logging.exception("Error!")
                logging.exception(e)
                logging.exception(traceback.format_exc())

            finally:
                self.incoming_msg_q.task_done()

    def route_message(self, whatsapp_body):
        self.routing_service.route_message(whatsapp_body)
