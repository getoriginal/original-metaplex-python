from solders.instruction import AccountMeta
from solders.pubkey import Pubkey

from src.token_metadata.generated.instructions import thaw_delegated_account
from src.token_metadata.generated.program_id import PROGRAM_ID


def test_thaw_delegated_account():
    accounts = {
        "delegate": Pubkey.new_unique(),
        "token_account": Pubkey.new_unique(),
        "edition": Pubkey.new_unique(),
        "mint": Pubkey.new_unique(),
    }
    instruction = thaw_delegated_account(accounts)
    assert instruction.program_id == PROGRAM_ID
    assert len(instruction.accounts) == 5
    assert isinstance(instruction.data, bytes)


def test_thaw_delegated_account_with_remaining_accounts():
    accounts = {
        "delegate": Pubkey.new_unique(),
        "token_account": Pubkey.new_unique(),
        "edition": Pubkey.new_unique(),
        "mint": Pubkey.new_unique(),
    }
    remaining_accounts = [
        AccountMeta(pubkey=Pubkey.new_unique(), is_signer=False, is_writable=False)
    ]
    instruction = thaw_delegated_account(
        accounts, remaining_accounts=remaining_accounts
    )
    assert len(instruction.accounts) == 5 + len(remaining_accounts)
