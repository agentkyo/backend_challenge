import string
import random


class Utilities:
    def __init__(self) -> None:
        self.password_string_length = 15

    def generate_random_password(
        self,
    ):
        """Generate a random password of fixed length"""
        letters = string.ascii_letters + string.digits + string.punctuation
        return "".join(
            random.choice(letters) for i in range(self.password_string_length)
        )
