from solders.instruction import AccountMeta
from solders.pubkey import Pubkey

from original_metaplex_python.token_metadata.generated.instructions import (
    set_collection_size,
)
from original_metaplex_python.token_metadata.generated.program_id import PROGRAM_ID
from original_metaplex_python.token_metadata.generated.types import (
    set_collection_size_args,
)


def test_set_collection_size():
    args = {
        "set_collection_size_args": set_collection_size_args.SetCollectionSizeArgs(
            size=1
        ),
    }
    accounts = {
        "collection_metadata": Pubkey.new_unique(),
        "collection_authority": Pubkey.new_unique(),
        "collection_mint": Pubkey.new_unique(),
        "collection_authority_record": None,
    }
    instruction = set_collection_size(args, accounts)
    assert instruction.program_id == PROGRAM_ID
    assert len(instruction.accounts) == 4
    assert isinstance(instruction.data, bytes)


def test_set_collection_size_with_remaining_accounts():
    args = {
        "set_collection_size_args": set_collection_size_args.SetCollectionSizeArgs(
            size=1
        ),
    }
    accounts = {
        "collection_metadata": Pubkey.new_unique(),
        "collection_authority": Pubkey.new_unique(),
        "collection_mint": Pubkey.new_unique(),
        "collection_authority_record": None,
    }
    remaining_accounts = [
        AccountMeta(pubkey=Pubkey.new_unique(), is_signer=False, is_writable=False)
    ]
    instruction = set_collection_size(
        args, accounts, remaining_accounts=remaining_accounts
    )
    assert len(instruction.accounts) == 5
