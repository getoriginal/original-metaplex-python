from solders.instruction import AccountMeta
from solders.pubkey import Pubkey

from original_metaplex_python.token_metadata.generated.instructions import (
    revoke_collection_authority,
)
from original_metaplex_python.token_metadata.generated.program_id import PROGRAM_ID


def test_revoke_collection_authority():
    accounts = {
        "collection_authority_record": Pubkey.new_unique(),
        "delegate_authority": Pubkey.new_unique(),
        "revoke_authority": Pubkey.new_unique(),
        "metadata": Pubkey.new_unique(),
        "mint": Pubkey.new_unique(),
    }
    instruction = revoke_collection_authority(accounts)
    assert instruction.program_id == PROGRAM_ID
    assert len(instruction.accounts) == 5
    assert isinstance(instruction.data, bytes)


def test_revoke_collection_authority_with_remaining_accounts():
    accounts = {
        "collection_authority_record": Pubkey.new_unique(),
        "delegate_authority": Pubkey.new_unique(),
        "revoke_authority": Pubkey.new_unique(),
        "metadata": Pubkey.new_unique(),
        "mint": Pubkey.new_unique(),
    }
    remaining_accounts = [
        AccountMeta(pubkey=Pubkey.new_unique(), is_signer=False, is_writable=False)
    ]
    instruction = revoke_collection_authority(
        accounts, remaining_accounts=remaining_accounts
    )
    assert len(instruction.accounts) == 5 + len(remaining_accounts)
