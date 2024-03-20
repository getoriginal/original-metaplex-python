import nacl.encoding
import nacl.signing
from solana.rpc.api import Keypair
from solana.transaction import Transaction


class KeypairIdentityDriver:
    def __init__(self, keypair: Keypair):
        self.keypair = keypair
        self.public_key = keypair.pubkey()
        self.secret_key = keypair.secret()

    def sign_message(self, message: bytes) -> bytes:
        signing_key = nacl.signing.SigningKey(
            self.secret_key[:32], encoder=nacl.encoding.RawEncoder
        )
        signed_message = signing_key.sign(message)
        return signed_message.signature

    def sign_transaction(self, transaction: Transaction) -> Transaction:
        transaction.sign_partial(self.keypair)
        return transaction

    def sign_all_transactions(
        self, transactions: list[Transaction]
    ) -> list[Transaction]:
        return [self.sign_transaction(tx) for tx in transactions]
