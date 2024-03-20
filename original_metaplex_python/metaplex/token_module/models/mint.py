from dataclasses import dataclass
from typing import Optional

from solders.pubkey import Pubkey
from solders.token.state import Mint as SplMint
from spl.token.constants import WRAPPED_SOL_MINT

from original_metaplex_python.metaplex.types.amount import (
    SplTokenAmount,
    SplTokenCurrency,
    spl_token_amount,
)


@dataclass
class Mint:
    model: str
    address: Pubkey
    decimals: int
    supply: SplTokenAmount
    is_wrapped_sol: bool
    currency: SplTokenCurrency
    mint_authority_address: Optional[Pubkey] = None
    freeze_authority_address: Optional[Pubkey] = None


def to_mint(mint_account, mint_public_key):
    is_wrapped_sol = mint_public_key == WRAPPED_SOL_MINT
    currency = SplTokenCurrency(
        symbol="SOL" if is_wrapped_sol else "Token",
        decimals=mint_account.decimals,
        namespace="spl-token",
    )

    return Mint(
        model="mint",
        address=mint_public_key,
        mint_authority_address=mint_account.mint_authority,
        freeze_authority_address=mint_account.freeze_authority,
        decimals=mint_account.decimals,
        supply=spl_token_amount(str(mint_account.supply), currency),
        is_wrapped_sol=is_wrapped_sol,
        currency=currency,
    )


def to_mint_account(account) -> SplMint:
    mint = SplMint.from_bytes(account.data)
    return mint
