from solders.instruction import AccountMeta
from solders.pubkey import Pubkey

from src.token_metadata.generated.instructions import revoke_use_authority
from src.token_metadata.generated.program_id import PROGRAM_ID


def test_revoke_use_authority():
    accounts = {
        "use_authority_record": Pubkey.new_unique(),
        "owner": Pubkey.new_unique(),
        "user": Pubkey.new_unique(),
        "owner_token_account": Pubkey.new_unique(),
        "mint": Pubkey.new_unique(),
        "metadata": Pubkey.new_unique(),
    }
    instruction = revoke_use_authority(accounts)
    assert instruction.program_id == PROGRAM_ID
    assert len(instruction.accounts) == 9
    assert isinstance(instruction.data, bytes)


def test_revoke_use_authority_with_remaining_accounts():
    accounts = {
        "use_authority_record": Pubkey.new_unique(),
        "owner": Pubkey.new_unique(),
        "user": Pubkey.new_unique(),
        "owner_token_account": Pubkey.new_unique(),
        "mint": Pubkey.new_unique(),
        "metadata": Pubkey.new_unique(),
    }
    remaining_accounts = [
        AccountMeta(pubkey=Pubkey.new_unique(), is_signer=False, is_writable=False)
    ]
    instruction = revoke_use_authority(accounts, remaining_accounts=remaining_accounts)
    assert len(instruction.accounts) == 10
