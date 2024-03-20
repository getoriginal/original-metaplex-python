from solders.instruction import AccountMeta
from solders.pubkey import Pubkey
from solders.system_program import ID as SYS_PROGRAM_ID
from solders.sysvar import RENT
from spl.token.constants import TOKEN_PROGRAM_ID

from original_metaplex_python.token_metadata.generated.instructions import (
    approve_use_authority,
)
from original_metaplex_python.token_metadata.generated.program_id import PROGRAM_ID
from original_metaplex_python.token_metadata.generated.types import (
    ApproveUseAuthorityArgs,
)


def test_approve_use_authority():
    args = {"approve_use_authority_args": ApproveUseAuthorityArgs(number_of_uses=3)}
    accounts = {
        "use_authority_record": Pubkey.new_unique(),
        "owner": Pubkey.new_unique(),
        "payer": Pubkey.new_unique(),
        "user": Pubkey.new_unique(),
        "owner_token_account": Pubkey.new_unique(),
        "metadata": Pubkey.new_unique(),
        "mint": Pubkey.new_unique(),
        "burner": Pubkey.new_unique(),
    }
    instruction = approve_use_authority(args, accounts)

    assert instruction.program_id == PROGRAM_ID
    assert len(instruction.accounts) == 11
    assert instruction.data.startswith(b"\x0e\x04M\x86V\x17%\xec")

    expected_keys = [
        AccountMeta(accounts["use_authority_record"], False, True),
        AccountMeta(accounts["owner"], True, True),
        AccountMeta(accounts["payer"], True, True),
        AccountMeta(accounts["user"], False, False),
        AccountMeta(accounts["owner_token_account"], False, True),
        AccountMeta(accounts["metadata"], False, False),
        AccountMeta(accounts["mint"], False, False),
        AccountMeta(accounts["burner"], False, False),
        AccountMeta(TOKEN_PROGRAM_ID, False, False),
        AccountMeta(SYS_PROGRAM_ID, False, False),
        (
            AccountMeta(RENT, False, False)
            if RENT
            else AccountMeta(PROGRAM_ID, False, False)
        ),
    ]

    for expected, actual in zip(expected_keys, instruction.accounts):
        assert expected.pubkey == actual.pubkey
        assert expected.is_signer == actual.is_signer
        assert expected.is_writable == actual.is_writable


def test_approve_use_authority_with_remaining_accounts():
    args = {"approve_use_authority_args": ApproveUseAuthorityArgs(number_of_uses=3)}
    accounts = {
        "use_authority_record": Pubkey.new_unique(),
        "owner": Pubkey.new_unique(),
        "payer": Pubkey.new_unique(),
        "user": Pubkey.new_unique(),
        "owner_token_account": Pubkey.new_unique(),
        "metadata": Pubkey.new_unique(),
        "mint": Pubkey.new_unique(),
        "burner": Pubkey.new_unique(),
    }
    remaining_accounts = [AccountMeta(Pubkey.new_unique(), False, True)]
    instruction = approve_use_authority(
        args, accounts, remaining_accounts=remaining_accounts
    )

    assert len(instruction.accounts) == 12
