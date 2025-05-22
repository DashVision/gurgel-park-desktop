import re

class Email:
    EMAIL_REGEX = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

    def __init__(self, address: str):
        if not self.is_valid(address):
            raise ValueError(f"Invalid email address: {address}")
        self.address = address

    @staticmethod
    def is_valid(email: str) -> bool:
        return re.match(Email.EMAIL_REGEX, email) is not None

    def get_domain(self) -> str:
        return self.address.split('@')[-1]

    def __str__(self):
        return self.address