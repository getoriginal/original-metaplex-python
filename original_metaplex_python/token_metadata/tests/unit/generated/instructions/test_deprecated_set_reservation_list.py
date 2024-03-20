from solders.instruction import AccountMeta
from solders.pubkey import Pubkey

from original_metaplex_python.token_metadata.generated.instructions import (
    deprecated_set_reservation_list,
)
from original_metaplex_python.token_metadata.generated.program_id import PROGRAM_ID


def test_deprecated_set_reservation_list():
    accounts = {
        "master_edition": Pubkey.new_unique(),
        "reservation_list": Pubkey.new_unique(),
        "resource": Pubkey.new_unique(),
    }
    instruction = deprecated_set_reservation_list(accounts)
    assert instruction.program_id == PROGRAM_ID
    assert len(instruction.accounts) == 3
    assert isinstance(instruction.data, bytes)


def test_deprecated_set_reservation_list_with_remaining_accounts():
    accounts = {
        "master_edition": Pubkey.new_unique(),
        "reservation_list": Pubkey.new_unique(),
        "resource": Pubkey.new_unique(),
    }
    remaining_accounts = [
        AccountMeta(pubkey=Pubkey.new_unique(), is_signer=False, is_writable=False)
    ]
    instruction = deprecated_set_reservation_list(
        accounts, remaining_accounts=remaining_accounts
    )
    assert len(instruction.accounts) == 4
