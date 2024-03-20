from solders.instruction import AccountMeta
from solders.pubkey import Pubkey

from original_metaplex_python.token_metadata.generated.instructions import (
    update_primary_sale_happened_via_token,
)
from original_metaplex_python.token_metadata.generated.program_id import PROGRAM_ID


def test_update_primary_sale_happened_via_token():
    accounts = {
        "metadata": Pubkey.new_unique(),
        "owner": Pubkey.new_unique(),
        "token": Pubkey.new_unique(),
    }
    instruction = update_primary_sale_happened_via_token(accounts)
    assert instruction.program_id == PROGRAM_ID
    assert len(instruction.accounts) == 3
    assert isinstance(instruction.data, bytes)


def test_update_primary_sale_happened_via_token_with_remaining_accounts():
    accounts = {
        "metadata": Pubkey.new_unique(),
        "owner": Pubkey.new_unique(),
        "token": Pubkey.new_unique(),
    }
    remaining_accounts = [
        AccountMeta(pubkey=Pubkey.new_unique(), is_signer=False, is_writable=False)
    ]
    instruction = update_primary_sale_happened_via_token(
        accounts, remaining_accounts=remaining_accounts
    )
    assert len(instruction.accounts) == 3 + len(remaining_accounts)
