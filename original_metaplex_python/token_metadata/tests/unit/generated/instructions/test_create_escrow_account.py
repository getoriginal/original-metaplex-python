from solders.instruction import AccountMeta
from solders.pubkey import Pubkey

from original_metaplex_python.token_metadata.generated.instructions.create_escrow_account import (
    create_escrow_account,
)
from original_metaplex_python.token_metadata.generated.program_id import PROGRAM_ID


def test_create_escrow_account():
    accounts = {
        "escrow": Pubkey.new_unique(),
        "metadata": Pubkey.new_unique(),
        "mint": Pubkey.new_unique(),
        "token_account": Pubkey.new_unique(),
        "edition": Pubkey.new_unique(),
        "payer": Pubkey.new_unique(),
        "sysvar_instructions": Pubkey.new_unique(),
        "authority": None,
    }
    instruction = create_escrow_account(accounts=accounts, program_id=PROGRAM_ID)
    assert len(instruction.accounts) == 9
    assert instruction.program_id == PROGRAM_ID


def test_create_escrow_account_with_authority():
    accounts = {
        "escrow": Pubkey.new_unique(),
        "metadata": Pubkey.new_unique(),
        "mint": Pubkey.new_unique(),
        "token_account": Pubkey.new_unique(),
        "edition": Pubkey.new_unique(),
        "payer": Pubkey.new_unique(),
        "sysvar_instructions": Pubkey.new_unique(),
        "authority": Pubkey.new_unique(),
    }
    instruction = create_escrow_account(accounts=accounts, program_id=PROGRAM_ID)
    assert len(instruction.accounts) == 9
    assert instruction.program_id == PROGRAM_ID


def test_create_escrow_account_with_remaining_accounts():
    additional_account = AccountMeta(
        pubkey=Pubkey.new_unique(), is_signer=False, is_writable=False
    )
    accounts = {
        "escrow": Pubkey.new_unique(),
        "metadata": Pubkey.new_unique(),
        "mint": Pubkey.new_unique(),
        "token_account": Pubkey.new_unique(),
        "edition": Pubkey.new_unique(),
        "payer": Pubkey.new_unique(),
        "sysvar_instructions": Pubkey.new_unique(),
        "authority": None,
    }
    instruction = create_escrow_account(
        accounts=accounts,
        program_id=PROGRAM_ID,
        remaining_accounts=[additional_account],
    )
    assert len(instruction.accounts) == 10
