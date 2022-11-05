from typing import Generator

from tenacity import AsyncRetrying, wait_fixed, stop_after_attempt
from requests.adapters import Retry

RETRIES = Retry(total=5, backoff_factor=0.5)
ASYNC_RETRIES = AsyncRetrying(wait=wait_fixed(5), stop=stop_after_attempt(5), reraise=True)
# Application key
APP_KEY = "1899"


# Connection retry generator
def attempts_generator(amount: int = 5):
    """
    Function generates a generator of length equal to `amount`

    Args:
        amount: number of attempts generated

    Returns:
        Attempt number
    """
    for i in range(1, amount):
        yield i
