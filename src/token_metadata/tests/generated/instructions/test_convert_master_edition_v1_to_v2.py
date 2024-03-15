from solders.instruction import AccountMeta
from solders.pubkey import Pubkey

from src.token_metadata.generated.instructions.convert_master_edition_v1_to_v2 import (
    convert_master_edition_v1_to_v2,
)
from src.token_metadata.generated.program_id import PROGRAM_ID


def test_convert_master_edition_v1_to_v2_basic():
    master_edition = Pubkey.new_unique()
    one_time_auth = Pubkey.new_unique()
    printing_mint = Pubkey.new_unique()

    instruction = convert_master_edition_v1_to_v2(
        accounts={
            "master_edition": master_edition,
            "one_time_auth": one_time_auth,
            "printing_mint": printing_mint,
        },
        program_id=PROGRAM_ID,
    )

    assert instruction.program_id == PROGRAM_ID
    assert len(instruction.accounts) == 3
    assert instruction.accounts[0].pubkey == master_edition
    assert instruction.accounts[1].pubkey == one_time_auth
    assert instruction.accounts[2].pubkey == printing_mint
    assert instruction.data == b"\xd9\x1al\x007~\xa7\xee" + b""


def test_convert_master_edition_v1_to_v2_with_remaining_accounts():
    master_edition = Pubkey.new_unique()
    one_time_auth = Pubkey.new_unique()
    printing_mint = Pubkey.new_unique()
    additional_account = AccountMeta(
        pubkey=Pubkey.new_unique(), is_signer=False, is_writable=False
    )

    instruction = convert_master_edition_v1_to_v2(
        accounts={
            "master_edition": master_edition,
            "one_time_auth": one_time_auth,
            "printing_mint": printing_mint,
        },
        program_id=PROGRAM_ID,
        remaining_accounts=[additional_account],
    )

    assert instruction.program_id == PROGRAM_ID
    assert len(instruction.accounts) == 4
    assert instruction.accounts[3].pubkey == additional_account.pubkey
