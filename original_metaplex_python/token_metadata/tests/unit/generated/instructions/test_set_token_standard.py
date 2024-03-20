from solders.instruction import AccountMeta
from solders.pubkey import Pubkey

from original_metaplex_python.token_metadata.generated.instructions import (
    set_token_standard,
)
from original_metaplex_python.token_metadata.generated.program_id import PROGRAM_ID


def test_set_token_standard():
    accounts = {
        "metadata": Pubkey.new_unique(),
        "update_authority": Pubkey.new_unique(),
        "mint": Pubkey.new_unique(),
        "edition": None,
    }
    instruction = set_token_standard(accounts)
    assert instruction.program_id == PROGRAM_ID
    assert len(instruction.accounts) == 4
    assert isinstance(instruction.data, bytes)


def test_set_token_standard_with_remaining_accounts():
    accounts = {
        "metadata": Pubkey.new_unique(),
        "update_authority": Pubkey.new_unique(),
        "mint": Pubkey.new_unique(),
        "edition": None,
    }
    remaining_accounts = [
        AccountMeta(pubkey=Pubkey.new_unique(), is_signer=False, is_writable=False)
    ]
    instruction = set_token_standard(accounts, remaining_accounts=remaining_accounts)
    assert len(instruction.accounts) == 5
