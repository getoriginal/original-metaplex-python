from typing import List, Union

from solders.pubkey import Pubkey


class Pda:
    bump: int
    pubkey: Pubkey

    def __init__(self, pubkey: Union[bytes, bytearray], bump: int):
        self.pubkey = Pubkey.from_bytes(pubkey)
        self.bump = bump

    def is_on_curve(self) -> bool:
        return self.pubkey.is_on_curve()

    def __str__(self) -> str:
        return str(self.pubkey)

    def __repr__(self) -> str:
        return repr(self.pubkey)

    def __bytes__(self) -> bytes:
        return bytes(self.pubkey)

    def __hash__(self) -> int:
        return hash(self.pubkey)

    def to_json(self) -> str:
        return self.pubkey.to_json()

    @staticmethod
    def find(program_id: Pubkey, seeds: List[Union[bytes, bytearray]]) -> Pubkey:
        public_key, bump = Pubkey.find_program_address(seeds, program_id)
        pda = Pda(bytes(public_key), bump)
        # TODO_ORIGINAL: We do not use the bump, so we will not return it
        return pda.pubkey
