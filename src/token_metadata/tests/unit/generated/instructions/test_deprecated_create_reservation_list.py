from solders.instruction import AccountMeta
from solders.pubkey import Pubkey

from src.token_metadata.generated.instructions import deprecated_create_reservation_list
from src.token_metadata.generated.program_id import PROGRAM_ID


def test_deprecated_create_reservation_list():
    accounts = {
        "reservation_list": Pubkey.new_unique(),
        "payer": Pubkey.new_unique(),
        "update_authority": Pubkey.new_unique(),
        "master_edition": Pubkey.new_unique(),
        "resource": Pubkey.new_unique(),
        "metadata": Pubkey.new_unique(),
    }
    instruction = deprecated_create_reservation_list(accounts)
    assert instruction.program_id == PROGRAM_ID
    assert len(instruction.accounts) == 8
    assert isinstance(instruction.data, bytes)


def test_deprecated_create_reservation_list_with_remaining_accounts():
    accounts = {
        "reservation_list": Pubkey.new_unique(),
        "payer": Pubkey.new_unique(),
        "update_authority": Pubkey.new_unique(),
        "master_edition": Pubkey.new_unique(),
        "resource": Pubkey.new_unique(),
        "metadata": Pubkey.new_unique(),
    }
    remaining_accounts = [
        AccountMeta(pubkey=Pubkey.new_unique(), is_signer=False, is_writable=False)
    ]
    instruction = deprecated_create_reservation_list(
        accounts, remaining_accounts=remaining_accounts
    )
    assert (
        len(instruction.accounts) == 9
    )  # Original accounts plus the remaining account
