from solders.instruction import AccountMeta
from solders.pubkey import Pubkey

from original_metaplex_python.token_metadata.generated.instructions import (
    remove_creator_verification,
)
from original_metaplex_python.token_metadata.generated.program_id import PROGRAM_ID


def test_remove_creator_verification():
    accounts = {
        "metadata": Pubkey.new_unique(),
        "creator": Pubkey.new_unique(),
    }
    instruction = remove_creator_verification(accounts)
    assert instruction.program_id == PROGRAM_ID
    assert len(instruction.accounts) == 2
    assert isinstance(instruction.data, bytes)


def test_remove_creator_verification_with_remaining_accounts():
    accounts = {
        "metadata": Pubkey.new_unique(),
        "creator": Pubkey.new_unique(),
    }
    remaining_accounts = [
        AccountMeta(pubkey=Pubkey.new_unique(), is_signer=False, is_writable=False)
    ]
    instruction = remove_creator_verification(
        accounts, remaining_accounts=remaining_accounts
    )
    assert len(instruction.accounts) == 3  # 2 accounts + 1 remaining account
