from solders.instruction import AccountMeta
from solders.pubkey import Pubkey

from src.token_metadata.generated.instructions import utilize
from src.token_metadata.generated.program_id import PROGRAM_ID
from src.token_metadata.generated.types import UtilizeArgs


def test_utilize():
    args = {
        "utilize_args": UtilizeArgs(number_of_uses=0),
    }
    accounts = {
        "metadata": Pubkey.new_unique(),
        "token_account": Pubkey.new_unique(),
        "mint": Pubkey.new_unique(),
        "use_authority": Pubkey.new_unique(),
        "owner": Pubkey.new_unique(),
        "ata_program": Pubkey.new_unique(),
        "use_authority_record": Pubkey.new_unique(),
        "burner": Pubkey.new_unique(),
    }

    instruction = utilize(args, accounts)
    assert instruction.program_id == PROGRAM_ID
    assert len(instruction.accounts) == 11
    assert isinstance(instruction.data, bytes)


def test_utilize_with_remaining_accounts():
    args = {
        "utilize_args": UtilizeArgs(number_of_uses=0),
    }
    accounts = {
        "metadata": Pubkey.new_unique(),
        "token_account": Pubkey.new_unique(),
        "mint": Pubkey.new_unique(),
        "use_authority": Pubkey.new_unique(),
        "owner": Pubkey.new_unique(),
        "ata_program": Pubkey.new_unique(),
        "use_authority_record": Pubkey.new_unique(),
        "burner": Pubkey.new_unique(),
    }
    remaining_accounts = [
        AccountMeta(pubkey=Pubkey.new_unique(), is_signer=False, is_writable=False)
    ]
    instruction = utilize(args, accounts, remaining_accounts=remaining_accounts)
    assert len(instruction.accounts) == 11 + len(remaining_accounts)
