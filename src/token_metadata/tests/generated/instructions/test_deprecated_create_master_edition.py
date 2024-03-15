from solders.instruction import AccountMeta
from solders.pubkey import Pubkey

from src.token_metadata.generated.instructions import deprecated_create_master_edition
from src.token_metadata.generated.program_id import PROGRAM_ID


def test_deprecated_create_master_edition():
    accounts = {
        "edition": Pubkey.new_unique(),
        "mint": Pubkey.new_unique(),
        "printing_mint": Pubkey.new_unique(),
        "one_time_printing_authorization_mint": Pubkey.new_unique(),
        "update_authority": Pubkey.new_unique(),
        "printing_mint_authority": Pubkey.new_unique(),
        "mint_authority": Pubkey.new_unique(),
        "metadata": Pubkey.new_unique(),
        "payer": Pubkey.new_unique(),
        "one_time_printing_authorization_mint_authority": Pubkey.new_unique(),
    }
    instruction = deprecated_create_master_edition(accounts)
    assert instruction.program_id == PROGRAM_ID
    assert len(instruction.accounts) == 13
    assert isinstance(instruction.data, bytes)


def test_deprecated_create_master_edition_with_remaining_accounts():
    accounts = {
        "edition": Pubkey.new_unique(),
        "mint": Pubkey.new_unique(),
        "printing_mint": Pubkey.new_unique(),
        "one_time_printing_authorization_mint": Pubkey.new_unique(),
        "update_authority": Pubkey.new_unique(),
        "printing_mint_authority": Pubkey.new_unique(),
        "mint_authority": Pubkey.new_unique(),
        "metadata": Pubkey.new_unique(),
        "payer": Pubkey.new_unique(),
        "one_time_printing_authorization_mint_authority": Pubkey.new_unique(),
    }
    remaining_accounts = [
        AccountMeta(pubkey=Pubkey.new_unique(), is_signer=False, is_writable=False)
    ]
    instruction = deprecated_create_master_edition(
        accounts, remaining_accounts=remaining_accounts
    )
    assert len(instruction.accounts) == 14
