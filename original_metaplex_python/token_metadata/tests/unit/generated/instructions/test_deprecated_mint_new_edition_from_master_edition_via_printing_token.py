from solders.instruction import AccountMeta
from solders.pubkey import Pubkey

from original_metaplex_python.token_metadata.generated.instructions import (
    deprecated_mint_new_edition_from_master_edition_via_printing_token,
)
from original_metaplex_python.token_metadata.generated.program_id import PROGRAM_ID


def test_deprecated_mint_new_edition_from_master_edition_via_printing_token():
    accounts = {
        "metadata": Pubkey.new_unique(),
        "edition": Pubkey.new_unique(),
        "master_edition": Pubkey.new_unique(),
        "mint": Pubkey.new_unique(),
        "mint_authority": Pubkey.new_unique(),
        "printing_mint": Pubkey.new_unique(),
        "master_token_account": Pubkey.new_unique(),
        "edition_marker": Pubkey.new_unique(),
        "burn_authority": Pubkey.new_unique(),
        "payer": Pubkey.new_unique(),
        "master_update_authority": Pubkey.new_unique(),
        "master_metadata": Pubkey.new_unique(),
        "reservation_list": None,
    }
    instruction = deprecated_mint_new_edition_from_master_edition_via_printing_token(
        accounts
    )
    assert instruction.program_id == PROGRAM_ID
    assert len(instruction.accounts) == 16
    assert isinstance(instruction.data, bytes)


def test_deprecated_mint_new_edition_from_master_edition_via_printing_token_with_remaining_accounts():
    accounts = {
        "metadata": Pubkey.new_unique(),
        "edition": Pubkey.new_unique(),
        "master_edition": Pubkey.new_unique(),
        "mint": Pubkey.new_unique(),
        "mint_authority": Pubkey.new_unique(),
        "printing_mint": Pubkey.new_unique(),
        "master_token_account": Pubkey.new_unique(),
        "edition_marker": Pubkey.new_unique(),
        "burn_authority": Pubkey.new_unique(),
        "payer": Pubkey.new_unique(),
        "master_update_authority": Pubkey.new_unique(),
        "master_metadata": Pubkey.new_unique(),
        "reservation_list": Pubkey.new_unique(),
    }
    remaining_accounts = [
        AccountMeta(pubkey=Pubkey.new_unique(), is_signer=False, is_writable=False)
    ]
    instruction = deprecated_mint_new_edition_from_master_edition_via_printing_token(
        accounts, remaining_accounts=remaining_accounts
    )
    assert (
        len(instruction.accounts) == 17
    )  # Original accounts plus the remaining account
