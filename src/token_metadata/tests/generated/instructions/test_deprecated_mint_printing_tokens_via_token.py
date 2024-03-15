from solders.instruction import AccountMeta
from solders.pubkey import Pubkey

from src.token_metadata.generated.instructions import (
    deprecated_mint_printing_tokens_via_token,
)
from src.token_metadata.generated.program_id import PROGRAM_ID


def test_deprecated_mint_printing_tokens_via_token():
    accounts = {
        "destination": Pubkey.new_unique(),
        "token": Pubkey.new_unique(),
        "one_time_printing_authorization_mint": Pubkey.new_unique(),
        "printing_mint": Pubkey.new_unique(),
        "burn_authority": Pubkey.new_unique(),
        "metadata": Pubkey.new_unique(),
        "master_edition": Pubkey.new_unique(),
    }
    instruction = deprecated_mint_printing_tokens_via_token(accounts)
    assert instruction.program_id == PROGRAM_ID
    assert len(instruction.accounts) == 9
    assert isinstance(instruction.data, bytes)


def test_deprecated_mint_printing_tokens_via_token_with_remaining_accounts():
    accounts = {
        "destination": Pubkey.new_unique(),
        "token": Pubkey.new_unique(),
        "one_time_printing_authorization_mint": Pubkey.new_unique(),
        "printing_mint": Pubkey.new_unique(),
        "burn_authority": Pubkey.new_unique(),
        "metadata": Pubkey.new_unique(),
        "master_edition": Pubkey.new_unique(),
    }
    remaining_accounts = [
        AccountMeta(pubkey=Pubkey.new_unique(), is_signer=False, is_writable=False)
    ]
    instruction = deprecated_mint_printing_tokens_via_token(
        accounts, remaining_accounts=remaining_accounts
    )
    assert len(instruction.accounts) == 10
