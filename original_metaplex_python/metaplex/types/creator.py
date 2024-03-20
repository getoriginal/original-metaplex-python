from dataclasses import dataclass
from typing import Optional

from solders.pubkey import Pubkey

from original_metaplex_python.metaplex.types.signer import Signer


@dataclass
class CreatorInput:
    address: Pubkey
    share: int
    authority: Optional[Signer] = None
    verified: Optional[bool] = None
