import json
import logging
import time
from typing import Callable, List, Literal
import requests

from .config import ALERTS_URL
from .types import Alert


def check_alert(areas: List[str] | Literal["all"] = "all"):
    logger = logging.getLogger(__name__)

    try:
        response = requests.get(ALERTS_URL).json()
        received_alert = Alert(**{**response, "relevant": areas,
                               "category": response.get("cat"), "description": response.get("desc")})
        logger.debug(">>> Received alert")

        # For debugging
        # print(">>> Received alert!")
        # print(str(received_alert))
        return received_alert

    except ValueError as e:
        return False

    except requests.exceptions.SSLError:
        logger.warning("[!] Couldn't reach server")


def listen(callback: Callable[..., None], areas: List[str] | Literal["all"] = "all", args: tuple = (), kwargs: dict = {}):
    logger = logging.getLogger(__name__)

    logger.info("[i] Started listening")
    alerts = {}

    while True:
        try:
            received_alert = check_alert(areas)
            if received_alert:
                if not received_alert.id in alerts:
                    logger.debug(">>> Raising alert")
                    callback(received_alert, *args, **kwargs)
                    alerts[received_alert.id] = time.time()

            now = time.time()
            alerts = {k: v for k, v in alerts.items() if now - v <= 900}
        except requests.exceptions.ConnectionError as e:
            logger.warning(f"[!] Error checking alerts: {e}")

        time.sleep(1)
