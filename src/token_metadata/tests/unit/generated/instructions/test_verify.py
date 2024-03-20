from solders.instruction import AccountMeta
from solders.pubkey import Pubkey

from src.token_metadata.generated.instructions import verify
from src.token_metadata.generated.program_id import PROGRAM_ID
from src.token_metadata.generated.types.verification_args import CreatorV1


def test_verify():
    args = {
        "verification_args": CreatorV1(),
    }
    accounts = {
        "authority": Pubkey.new_unique(),
        "delegate_record": Pubkey.new_unique(),
        "metadata": Pubkey.new_unique(),
        "collection_mint": Pubkey.new_unique(),
        "collection_metadata": Pubkey.new_unique(),
        "collection_master_edition": Pubkey.new_unique(),
        "sysvar_instructions": Pubkey.new_unique(),
    }

    instruction = verify(args, accounts)
    assert instruction.program_id == PROGRAM_ID
    assert len(instruction.accounts) == 8
    assert isinstance(instruction.data, bytes)


def test_verify_with_remaining_accounts():
    args = {
        "verification_args": CreatorV1(),
    }
    accounts = {
        "authority": Pubkey.new_unique(),
        "delegate_record": Pubkey.new_unique(),
        "metadata": Pubkey.new_unique(),
        "collection_mint": Pubkey.new_unique(),
        "collection_metadata": Pubkey.new_unique(),
        "collection_master_edition": Pubkey.new_unique(),
        "sysvar_instructions": Pubkey.new_unique(),
    }

    remaining_accounts = [
        AccountMeta(pubkey=Pubkey.new_unique(), is_signer=False, is_writable=False)
    ]
    instruction = verify(args, accounts, remaining_accounts=remaining_accounts)
    assert len(instruction.accounts) == 8 + len(remaining_accounts)
