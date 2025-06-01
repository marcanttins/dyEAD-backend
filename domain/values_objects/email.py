# backend/domain/value_objects/email_dto.py
import re

class Email:
    _pattern = re.compile(r"^[\w.-]+@[\w.-]+\.\w+$")

    def __init__(self, address: str):
        if not self._pattern.match(address):
            raise ValueError(f"Email inválido: {address}")
        self._address = address.lower()

    @property
    def address(self) -> str:
        return self._address

    def __eq__(self, other):
        return isinstance(other, Email) and self.address == other.address

    def __str__(self):
        return self.address
