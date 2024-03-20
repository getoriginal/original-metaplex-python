from solders.instruction import AccountMeta
from solders.pubkey import Pubkey
from solders.system_program import ID as SYS_PROGRAM_ID

from original_metaplex_python.token_metadata.generated.instructions import burn
from original_metaplex_python.token_metadata.generated.program_id import PROGRAM_ID
from original_metaplex_python.token_metadata.generated.types.burn_args import (
    BurnArgsKind,
    V1Value,
)


def test_burn():
    args = {"burn_args": BurnArgsKind(V1Value(amount=42))}
    accounts = {
        "authority": Pubkey.new_unique(),
        "collection_metadata": Pubkey.new_unique(),
        "metadata": Pubkey.new_unique(),
        "edition": Pubkey.new_unique(),
        "mint": Pubkey.new_unique(),
        "token": Pubkey.new_unique(),
        "master_edition": Pubkey.new_unique(),
        "master_edition_mint": Pubkey.new_unique(),
        "master_edition_token": Pubkey.new_unique(),
        "edition_marker": Pubkey.new_unique(),
        "token_record": Pubkey.new_unique(),
        "sysvar_instructions": SYS_PROGRAM_ID,
        "spl_token_program": Pubkey.new_unique(),
    }
    instruction = burn(args, accounts)

    assert instruction.program_id == PROGRAM_ID
    assert len(instruction.accounts) == 14
    assert instruction.data.startswith(bytes([41]))

    # Validate keys
    expected_keys = [
        AccountMeta(accounts["authority"], True, True),
        AccountMeta(accounts["collection_metadata"], False, True),
        AccountMeta(accounts["metadata"], False, True),
        AccountMeta(accounts["edition"], False, True),
        AccountMeta(accounts["mint"], False, True),
        AccountMeta(accounts["token"], False, True),
        AccountMeta(accounts["master_edition"], False, True),
        AccountMeta(accounts["master_edition_mint"], False, False),
        AccountMeta(accounts["master_edition_token"], False, False),
        AccountMeta(accounts["edition_marker"], False, True),
        AccountMeta(accounts["token_record"], False, True),
        AccountMeta(SYS_PROGRAM_ID, False, False),
        AccountMeta(accounts["sysvar_instructions"], False, False),
        AccountMeta(accounts["spl_token_program"], False, False),
    ]

    for expected, actual in zip(expected_keys, instruction.accounts):
        assert expected.pubkey == actual.pubkey
        assert expected.is_signer == actual.is_signer
        assert expected.is_writable == actual.is_writable


def test_burn_with_optional_accounts_none():
    args = {"burn_args": BurnArgsKind(V1Value(amount=42))}
    accounts = {
        "authority": Pubkey.new_unique(),
        "collection_metadata": None,
        "metadata": Pubkey.new_unique(),
        "edition": None,
        "mint": Pubkey.new_unique(),
        "token": Pubkey.new_unique(),
        "master_edition": None,
        "master_edition_mint": None,
        "master_edition_token": None,
        "edition_marker": None,
        "token_record": None,
        "sysvar_instructions": SYS_PROGRAM_ID,
        "spl_token_program": Pubkey.new_unique(),
    }
    instruction = burn(args, accounts)

    assert len(instruction.accounts) == 14
    for account_meta in instruction.accounts:
        if account_meta.pubkey == PROGRAM_ID:
            assert not account_meta.is_writable
            break
    else:
        assert False, "Optional account missing or not set to default."
