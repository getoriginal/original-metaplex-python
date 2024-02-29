from typing import Union

import ed25519
from solana.transaction import Transaction
from solders.pubkey import Pubkey

from ..errors.sdk_error import DriverNotProvidedError
from ..types.signer import Signer
from .identity_driver import IdentityDriver


class IdentityClient:
    def __init__(self):
        self._driver = None

    def driver(self) -> IdentityDriver:
        if not self._driver:
            raise DriverNotProvidedError("IdentityDriver")
        return self._driver

    def set_driver(self, new_driver: IdentityDriver):
        self._driver = new_driver

    @property
    def public_key(self) -> Pubkey:
        return self.driver().public_key

    @property
    def secret_key(self) -> Union[bytes, None]:
        return self.driver().secret_key

    def sign_message(self, message: bytes) -> bytes:
        return self.driver().sign_message(message)

    def sign_transaction(self, transaction: Transaction) -> Transaction:
        return self.driver().sign_transaction(transaction)

    def sign_all_transactions(
        self, transactions: list[Transaction]
    ) -> list[Transaction]:
        return self.driver().sign_all_transactions(transactions)

    def verify_message(self, message: bytes, signature: bytes) -> bool:
        return ed25519.sync.verify(message, signature, bytes(self.public_key))

    def equals(self, that: Union[Signer, Pubkey]) -> bool:
        if hasattr(that, "public_key"):
            that = that.public_key
        return self.public_key == that

    def has_secret_key(self) -> bool:
        return self.secret_key is not None
