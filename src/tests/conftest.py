import random
import string


class CoreTest:
    RUCAPTCHA_KEY = "ad9053f3182ca81755768608fa758570"

    def get_random_string(self, length):
        # choose from all lowercase letter
        letters = string.ascii_lowercase
        result_str = "".join(random.choice(letters) for i in range(length))
        print("Random string of length", length, "is:", result_str)
