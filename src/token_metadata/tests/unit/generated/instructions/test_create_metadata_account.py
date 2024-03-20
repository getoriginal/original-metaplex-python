from solders.instruction import AccountMeta
from solders.pubkey import Pubkey

from src.token_metadata.generated.instructions.create_metadata_account import (
    create_metadata_account,
)
from src.token_metadata.generated.program_id import PROGRAM_ID


def test_create_metadata_account():
    accounts = {
        "metadata": Pubkey.new_unique(),
        "mint": Pubkey.new_unique(),
        "mint_authority": Pubkey.new_unique(),
        "payer": Pubkey.new_unique(),
        "update_authority": Pubkey.new_unique(),
    }
    instruction = create_metadata_account(accounts=accounts, program_id=PROGRAM_ID)
    assert len(instruction.accounts) == 7
    assert instruction.program_id == PROGRAM_ID


def test_create_metadata_account_with_remaining_accounts():
    additional_account = AccountMeta(
        pubkey=Pubkey.new_unique(), is_signer=False, is_writable=False
    )
    accounts = {
        "metadata": Pubkey.new_unique(),
        "mint": Pubkey.new_unique(),
        "mint_authority": Pubkey.new_unique(),
        "payer": Pubkey.new_unique(),
        "update_authority": Pubkey.new_unique(),
    }
    instruction = create_metadata_account(
        accounts=accounts,
        program_id=PROGRAM_ID,
        remaining_accounts=[additional_account],
    )
    assert len(instruction.accounts) == 8
