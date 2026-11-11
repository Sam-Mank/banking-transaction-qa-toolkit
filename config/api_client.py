import requests
import logging

from config.settings import API_BASE_URL, REQUEST_TIMEOUT
from config.logging_config import *

logger = logging.getLogger(__name__)


def create_transaction(payload):

    logger.info("Sending transaction creation request")

    response = requests.post(
        f"{API_BASE_URL}/transactions",
        json=payload,
        timeout=REQUEST_TIMEOUT
    )

    logger.info(
        "Transaction request completed with status code: %s",
        response.status_code
    )

    return response