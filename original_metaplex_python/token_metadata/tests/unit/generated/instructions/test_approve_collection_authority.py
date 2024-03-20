from solders.instruction import AccountMeta
from solders.pubkey import Pubkey
from solders.system_program import ID as SYS_PROGRAM_ID
from solders.sysvar import RENT

from original_metaplex_python.token_metadata.generated.instructions.approve_collection_authority import (
    PROGRAM_ID,
    approve_collection_authority,
)


def test_approve_collection_authority():
    accounts = {
        "collection_authority_record": Pubkey.new_unique(),
        "new_collection_authority": Pubkey.new_unique(),
        "update_authority": Pubkey.new_unique(),
        "payer": Pubkey.new_unique(),
        "metadata": Pubkey.new_unique(),
        "mint": Pubkey.new_unique(),
    }
    instruction = approve_collection_authority(accounts)

    assert instruction.program_id == PROGRAM_ID
    assert len(instruction.accounts) == 8
    assert instruction.data[:8] == b"\xfe\x88\xd0'AB\x1bo"

    expected_keys = [
        AccountMeta(accounts["collection_authority_record"], False, True),
        AccountMeta(accounts["new_collection_authority"], False, False),
        AccountMeta(accounts["update_authority"], True, True),
        AccountMeta(accounts["payer"], True, True),
        AccountMeta(accounts["metadata"], False, False),
        AccountMeta(accounts["mint"], False, False),
        AccountMeta(SYS_PROGRAM_ID, False, False),
        (
            AccountMeta(RENT, False, False)
            if RENT
            else AccountMeta(PROGRAM_ID, False, False)
        ),
    ]

    for i, key in enumerate(expected_keys):
        assert instruction.accounts[i].pubkey == key.pubkey
        assert instruction.accounts[i].is_signer == key.is_signer
        assert instruction.accounts[i].is_writable == key.is_writable


def test_approve_collection_authority_with_remaining_accounts():
    accounts = {
        "collection_authority_record": Pubkey.new_unique(),
        "new_collection_authority": Pubkey.new_unique(),
        "update_authority": Pubkey.new_unique(),
        "payer": Pubkey.new_unique(),
        "metadata": Pubkey.new_unique(),
        "mint": Pubkey.new_unique(),
    }
    remaining_accounts = [AccountMeta(Pubkey.new_unique(), False, True)]
    instruction = approve_collection_authority(
        accounts, remaining_accounts=remaining_accounts
    )

    assert len(instruction.accounts) == 9
