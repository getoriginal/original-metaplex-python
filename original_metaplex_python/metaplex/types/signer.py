from abc import ABC, abstractmethod
from typing import List, Union

from solana.transaction import Transaction
from solders.pubkey import Pubkey


class KeypairSigner:
    public_key: Pubkey
    secret_key: bytes


class IdentitySigner(ABC):
    public_key: Pubkey

    @abstractmethod
    def sign_message(self, message: bytes) -> bytes:
        pass

    @abstractmethod
    def sign_transaction(self, transaction: Transaction) -> Transaction:
        pass

    @abstractmethod
    def sign_all_transactions(
        self, transactions: List[Transaction]
    ) -> List[Transaction]:
        pass


Signer = Union[KeypairSigner, IdentitySigner]


def is_signer(input):
    if isinstance(input, dict):
        return "public_key" in input and (
            "secret_key" in input or "sign_transaction" in input
        )
    else:
        has_public_key = hasattr(input, "public_key")
        has_secret_key = hasattr(input, "secret_key")
        has_sign_transaction = hasattr(input, "sign_transaction")
        return has_public_key and (has_secret_key or has_sign_transaction)


def is_keypair_signer(input):
    if is_signer(input):
        if isinstance(input, dict):
            ret_val = "secret_key" in input and input["secret_key"] is not None
            return ret_val
        else:
            ret_val = getattr(input, "secret_key") is not None
            return ret_val
    return False


def is_identity_signer(input):
    return is_signer(input) and not is_keypair_signer(input)


class SignerHistogram:
    def __init__(self):
        self.all = []
        self.keypairs = []
        self.identities = []


def get_public_key(obj):
    """Get the public key from the object, whether it's under 'public_key' or 'pubkey'."""
    if hasattr(obj, "public_key"):
        return obj.public_key
    elif hasattr(obj, "pubkey"):
        return obj.pubkey()
    else:
        return obj


def get_signer_histogram(signers: list[Signer]):
    signer_histogram = SignerHistogram()

    flattened_signers = [
        signer
        for sublist in signers
        for signer in (sublist if isinstance(sublist, list) else [sublist])
    ]

    for signer in flattened_signers:
        duplicate_index = next(
            (
                i
                for i, s in enumerate(signer_histogram.all)
                if get_public_key(s) == get_public_key(signer)
            ),
            None,
        )
        duplicate = (
            signer_histogram.all[duplicate_index]
            if duplicate_index is not None
            else None
        )
        duplicate_is_identity = is_identity_signer(duplicate) if duplicate else False
        signer_is_identity = is_identity_signer(signer)

        if duplicate is None:
            signer_histogram.all.append(signer)
            if signer_is_identity:
                signer_histogram.identities.append(signer)
            else:
                signer_histogram.keypairs.append(signer)
        elif duplicate_is_identity and not signer_is_identity:
            # Replace identity signer with keypair signer.
            signer_histogram.all[duplicate_index] = signer
            signer_histogram.keypairs.append(signer)
            signer_histogram.identities.remove(duplicate)

    return signer_histogram
