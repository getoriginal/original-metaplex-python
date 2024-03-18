from solders.instruction import AccountMeta
from solders.pubkey import Pubkey

from src.token_metadata.generated.instructions import puff_metadata
from src.token_metadata.generated.program_id import PROGRAM_ID


def test_puff_metadata():
    accounts = {"metadata": Pubkey.new_unique()}
    instruction = puff_metadata(accounts)
    assert instruction.program_id == PROGRAM_ID
    assert len(instruction.accounts) == 1
    assert isinstance(instruction.data, bytes)


def test_puff_metadata_with_remaining_accounts():
    accounts = {"metadata": Pubkey.new_unique()}
    remaining_accounts = [
        AccountMeta(pubkey=Pubkey.new_unique(), is_signer=False, is_writable=False)
    ]
    instruction = puff_metadata(accounts, remaining_accounts=remaining_accounts)
    assert len(instruction.accounts) == 2  # 1 account + 1 remaining account
