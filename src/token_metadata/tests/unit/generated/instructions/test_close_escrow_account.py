from solders.instruction import AccountMeta
from solders.pubkey import Pubkey

from src.token_metadata.generated.instructions import close_escrow_account
from src.token_metadata.generated.program_id import PROGRAM_ID


def test_close_escrow_account():
    accounts = {
        "escrow": Pubkey.new_unique(),
        "metadata": Pubkey.new_unique(),
        "mint": Pubkey.new_unique(),
        "token_account": Pubkey.new_unique(),
        "edition": Pubkey.new_unique(),
        "payer": Pubkey.new_unique(),
        "sysvar_instructions": Pubkey.new_unique(),
    }
    instruction = close_escrow_account(accounts)

    assert instruction.program_id == PROGRAM_ID
    assert len(instruction.accounts) == 8


def test_close_escrow_account_with_remaining_accounts():
    accounts = {
        "escrow": Pubkey.new_unique(),
        "metadata": Pubkey.new_unique(),
        "mint": Pubkey.new_unique(),
        "token_account": Pubkey.new_unique(),
        "edition": Pubkey.new_unique(),
        "payer": Pubkey.new_unique(),
        "sysvar_instructions": Pubkey.new_unique(),
    }
    remaining_accounts = [
        AccountMeta(Pubkey.new_unique(), is_signer=False, is_writable=False),
    ]
    instruction = close_escrow_account(accounts, remaining_accounts=remaining_accounts)

    assert len(instruction.accounts) == 8 + len(remaining_accounts)
