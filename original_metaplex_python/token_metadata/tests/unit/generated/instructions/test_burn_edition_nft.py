from solders.instruction import AccountMeta
from solders.pubkey import Pubkey

from original_metaplex_python.token_metadata.generated.instructions import (
    burn_edition_nft,
)
from original_metaplex_python.token_metadata.generated.program_id import PROGRAM_ID


def test_burn_edition_nft():
    accounts = {
        "metadata": Pubkey.new_unique(),
        "owner": Pubkey.new_unique(),
        "print_edition_mint": Pubkey.new_unique(),
        "master_edition_mint": Pubkey.new_unique(),
        "print_edition_token_account": Pubkey.new_unique(),
        "master_edition_token_account": Pubkey.new_unique(),
        "master_edition_account": Pubkey.new_unique(),
        "print_edition_account": Pubkey.new_unique(),
        "edition_marker_account": Pubkey.new_unique(),
        "spl_token_program": Pubkey.new_unique(),
    }
    instruction = burn_edition_nft(accounts)

    assert instruction.program_id == PROGRAM_ID
    assert len(instruction.accounts) == 10
    assert instruction.data.startswith(b"\xddi\xc4@\xa4\x1b]\xc5")

    # Validate keys
    expected_keys = [
        AccountMeta(accounts["metadata"], False, True),
        AccountMeta(accounts["owner"], True, True),
        AccountMeta(accounts["print_edition_mint"], False, True),
        AccountMeta(accounts["master_edition_mint"], False, False),
        AccountMeta(accounts["print_edition_token_account"], False, True),
        AccountMeta(accounts["master_edition_token_account"], False, False),
        AccountMeta(accounts["master_edition_account"], False, True),
        AccountMeta(accounts["print_edition_account"], False, True),
        AccountMeta(accounts["edition_marker_account"], False, True),
        AccountMeta(accounts["spl_token_program"], False, False),
    ]

    for expected, actual in zip(expected_keys, instruction.accounts):
        assert expected.pubkey == actual.pubkey
        assert expected.is_signer == actual.is_signer
        assert expected.is_writable == actual.is_writable


def test_burn_edition_nft_with_remaining_accounts():
    accounts = {
        "metadata": Pubkey.new_unique(),
        "owner": Pubkey.new_unique(),
        "print_edition_mint": Pubkey.new_unique(),
        "master_edition_mint": Pubkey.new_unique(),
        "print_edition_token_account": Pubkey.new_unique(),
        "master_edition_token_account": Pubkey.new_unique(),
        "master_edition_account": Pubkey.new_unique(),
        "print_edition_account": Pubkey.new_unique(),
        "edition_marker_account": Pubkey.new_unique(),
        "spl_token_program": Pubkey.new_unique(),
    }
    remaining_accounts = [
        AccountMeta(Pubkey.new_unique(), is_signer=False, is_writable=False),
    ]
    instruction = burn_edition_nft(accounts, remaining_accounts=remaining_accounts)

    assert len(instruction.accounts) == 11
