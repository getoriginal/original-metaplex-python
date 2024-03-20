from solders.instruction import AccountMeta
from solders.pubkey import Pubkey

from original_metaplex_python.token_metadata.generated.instructions import (
    bubblegum_set_collection_size,
)
from original_metaplex_python.token_metadata.generated.program_id import PROGRAM_ID
from original_metaplex_python.token_metadata.generated.types.set_collection_size_args import (
    SetCollectionSizeArgs,
)


def test_bubblegum_set_collection_size():
    args = {"set_collection_size_args": SetCollectionSizeArgs(size=100)}
    accounts = {
        "collection_metadata": Pubkey.new_unique(),
        "collection_authority": Pubkey.new_unique(),
        "collection_mint": Pubkey.new_unique(),
        "bubblegum_signer": Pubkey.new_unique(),
        "collection_authority_record": Pubkey.new_unique(),
    }
    instruction = bubblegum_set_collection_size(args, accounts)

    assert instruction.program_id == PROGRAM_ID
    assert len(instruction.accounts) == 5
    assert instruction.data.startswith(b"\xe6\xd7\xe7\xe2\x9c\xbc8\x06")

    # Validate keys
    expected_keys = [
        AccountMeta(accounts["collection_metadata"], False, True),
        AccountMeta(accounts["collection_authority"], True, False),
        AccountMeta(accounts["collection_mint"], False, False),
        AccountMeta(accounts["bubblegum_signer"], True, False),
        (
            AccountMeta(accounts["collection_authority_record"], False, False)
            if accounts["collection_authority_record"]
            else AccountMeta(PROGRAM_ID, False, False)
        ),
    ]

    for expected, actual in zip(expected_keys, instruction.accounts):
        assert expected.pubkey == actual.pubkey
        assert expected.is_signer == actual.is_signer
        assert expected.is_writable == actual.is_writable


def test_bubblegum_set_collection_size_without_collection_authority_record():
    args = {"set_collection_size_args": SetCollectionSizeArgs(size=100)}
    accounts = {
        "collection_metadata": Pubkey.new_unique(),
        "collection_authority": Pubkey.new_unique(),
        "collection_mint": Pubkey.new_unique(),
        "bubblegum_signer": Pubkey.new_unique(),
        "collection_authority_record": None,
    }
    instruction = bubblegum_set_collection_size(args, accounts)

    assert len(instruction.accounts) == 5
    assert instruction.accounts[4].pubkey == PROGRAM_ID
