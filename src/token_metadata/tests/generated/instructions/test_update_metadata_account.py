from solders.instruction import AccountMeta
from solders.pubkey import Pubkey

from src.token_metadata.generated.instructions import update_metadata_account
from src.token_metadata.generated.program_id import PROGRAM_ID


def test_update_metadata_account():
    accounts = {
        "metadata": Pubkey.new_unique(),
        "update_authority": Pubkey.new_unique(),
    }
    instruction = update_metadata_account(accounts)
    assert instruction.program_id == PROGRAM_ID
    assert len(instruction.accounts) == 2
    assert isinstance(instruction.data, bytes)


def test_update_metadata_account_with_remaining_accounts():
    accounts = {
        "metadata": Pubkey.new_unique(),
        "update_authority": Pubkey.new_unique(),
    }
    remaining_accounts = [
        AccountMeta(pubkey=Pubkey.new_unique(), is_signer=False, is_writable=False)
    ]
    instruction = update_metadata_account(
        accounts, remaining_accounts=remaining_accounts
    )
    assert len(instruction.accounts) == 3
