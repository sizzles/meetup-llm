from dataclasses import dataclass
import json
from typing import Optional
import logging


@dataclass
class Order:
    """Basic domain object for mapping an order reponse to a concrete object."""
    has_order: bool
    order_details: Optional[str]

    @staticmethod
    def from_response(response: str) -> Optional["Order"]:
        try:
            order = json.loads(response)
            has_order = order.get("has_order")
            order_details = order.get("order_details")
            return Order(has_order, order_details)
        except Exception as e:
            logging.exception(f"Could not parse order resonse to json.")
            logging.exception(e)
            return None
