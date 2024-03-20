from solders.instruction import AccountMeta
from solders.pubkey import Pubkey

from original_metaplex_python.token_metadata.generated.instructions import sign_metadata
from original_metaplex_python.token_metadata.generated.program_id import PROGRAM_ID


def test_sign_metadata():
    accounts = {
        "metadata": Pubkey.new_unique(),
        "creator": Pubkey.new_unique(),
    }
    instruction = sign_metadata(accounts)
    assert instruction.program_id == PROGRAM_ID
    assert len(instruction.accounts) == 2
    assert isinstance(instruction.data, bytes)


def test_sign_metadata_with_remaining_accounts():
    accounts = {
        "metadata": Pubkey.new_unique(),
        "creator": Pubkey.new_unique(),
    }
    remaining_accounts = [
        AccountMeta(pubkey=Pubkey.new_unique(), is_signer=False, is_writable=False)
    ]
    instruction = sign_metadata(accounts, remaining_accounts=remaining_accounts)
    assert len(instruction.accounts) == 2 + len(remaining_accounts)
