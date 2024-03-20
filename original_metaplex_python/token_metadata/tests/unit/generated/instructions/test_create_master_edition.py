from solders.instruction import AccountMeta
from solders.pubkey import Pubkey
from solders.system_program import ID as SYS_PROGRAM_ID
from solders.sysvar import RENT
from spl.token.constants import TOKEN_PROGRAM_ID

from original_metaplex_python.token_metadata.generated.instructions.create_master_edition import (
    create_master_edition,
)
from original_metaplex_python.token_metadata.generated.program_id import PROGRAM_ID


def test_create_master_edition():
    accounts = {
        "edition": Pubkey.new_unique(),
        "mint": Pubkey.new_unique(),
        "update_authority": Pubkey.new_unique(),
        "mint_authority": Pubkey.new_unique(),
        "payer": Pubkey.new_unique(),
        "metadata": Pubkey.new_unique(),
    }
    instruction = create_master_edition(accounts=accounts, program_id=PROGRAM_ID)
    assert len(instruction.accounts) == 9
    assert instruction.program_id == PROGRAM_ID
    assert instruction.accounts[6].pubkey == TOKEN_PROGRAM_ID
    assert instruction.accounts[7].pubkey == SYS_PROGRAM_ID
    assert instruction.accounts[8].pubkey == RENT


def test_create_master_edition_with_remaining_accounts():
    additional_account = AccountMeta(
        pubkey=Pubkey.new_unique(), is_signer=False, is_writable=False
    )
    accounts = {
        "edition": Pubkey.new_unique(),
        "mint": Pubkey.new_unique(),
        "update_authority": Pubkey.new_unique(),
        "mint_authority": Pubkey.new_unique(),
        "payer": Pubkey.new_unique(),
        "metadata": Pubkey.new_unique(),
    }
    instruction = create_master_edition(
        accounts=accounts,
        program_id=PROGRAM_ID,
        remaining_accounts=[additional_account],
    )
    assert len(instruction.accounts) == 10
    assert instruction.program_id == PROGRAM_ID
