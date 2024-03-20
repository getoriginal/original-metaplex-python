from dataclasses import dataclass
from typing import Optional

from solders.pubkey import Pubkey
from solders.token.state import TokenAccount, TokenAccountState

from original_metaplex_python.metaplex.token_module.program import (
    associated_token_program,
)
from original_metaplex_python.metaplex.types.amount import SplTokenAmount, token
from original_metaplex_python.metaplex.types.pda import Pda


@dataclass
class Token:
    model: str
    address: Pubkey
    is_associated_token: bool
    mint_address: Pubkey
    owner_address: Pubkey
    amount: SplTokenAmount
    close_authority_address: Optional[Pubkey]
    delegate_address: Optional[Pubkey]
    delegate_amount: SplTokenAmount
    state: TokenAccountState


def to_token(account: TokenAccount, public_key: Pubkey) -> Token:
    associated_token_address = Pda.find(
        associated_token_program.address,
        [bytes(account.owner), bytes(account.owner), bytes(account.mint)],
    )
    is_associated_token = associated_token_address == public_key

    return Token(
        model="token",
        address=associated_token_address if is_associated_token else public_key,
        is_associated_token=is_associated_token,
        mint_address=account.mint,
        owner_address=account.owner,
        amount=token(account.amount),
        close_authority_address=account.close_authority,
        delegate_address=account.delegate,
        delegate_amount=token(account.delegated_amount),
        state=account.state,
    )
