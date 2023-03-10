import os
import time
import random
import string

import pytest


@pytest.fixture(scope="function")
def delay():
    time.sleep(2)


@pytest.mark.usefixtures("delay")
class CoreTest:
    RUCAPTCHA_KEY = os.getenv("RUCAPTCHA_KEY", "ad9053f3182ca81755768608fa758570")
    sleep_time = 5

    proxyAddress = "0.0.0.0"
    proxyPort = 9999

    def get_random_string(self, length: int) -> str:
        """
        Method generate random string with set length
        : param length: Len of generated string
        : return: Random letter string
        """
        # choose from all lowercase letter
        letters = string.ascii_lowercase
        result_str = "".join(random.choice(letters) for _ in range(length))
        return result_str
