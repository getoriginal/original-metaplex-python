from dataclasses import dataclass
from typing import Optional

from solders.pubkey import Pubkey

from src.metaplex.types.signer import Signer


@dataclass
class CreatorInput:
    address: Pubkey
    share: int
    authority: Optional[Signer] = None
    verified: Optional[bool] = None
