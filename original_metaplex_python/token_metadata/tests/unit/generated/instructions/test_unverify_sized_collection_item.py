from solders.instruction import AccountMeta
from solders.pubkey import Pubkey

from original_metaplex_python.token_metadata.generated.instructions import (
    unverify_sized_collection_item,
)
from original_metaplex_python.token_metadata.generated.program_id import PROGRAM_ID


def test_unverify_sized_collection_item():
    accounts = {
        "metadata": Pubkey.new_unique(),
        "collection_authority": Pubkey.new_unique(),
        "payer": Pubkey.new_unique(),
        "collection_mint": Pubkey.new_unique(),
        "collection": Pubkey.new_unique(),
        "collection_master_edition_account": Pubkey.new_unique(),
        "collection_authority_record": Pubkey.new_unique(),
    }
    instruction = unverify_sized_collection_item(accounts)
    assert instruction.program_id == PROGRAM_ID
    assert len(instruction.accounts) == 7
    assert isinstance(instruction.data, bytes)


def test_unverify_sized_collection_item_with_remaining_accounts():
    accounts = {
        "metadata": Pubkey.new_unique(),
        "collection_authority": Pubkey.new_unique(),
        "payer": Pubkey.new_unique(),
        "collection_mint": Pubkey.new_unique(),
        "collection": Pubkey.new_unique(),
        "collection_master_edition_account": Pubkey.new_unique(),
        "collection_authority_record": Pubkey.new_unique(),
    }
    remaining_accounts = [
        AccountMeta(pubkey=Pubkey.new_unique(), is_signer=False, is_writable=False)
    ]
    instruction = unverify_sized_collection_item(
        accounts, remaining_accounts=remaining_accounts
    )
    assert len(instruction.accounts) == 7 + len(remaining_accounts)
