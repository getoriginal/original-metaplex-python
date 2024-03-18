from solders.instruction import AccountMeta
from solders.pubkey import Pubkey

from src.token_metadata.generated.instructions import unlock
from src.token_metadata.generated.program_id import PROGRAM_ID
from src.token_metadata.generated.types import AuthorizationData, Payload
from src.token_metadata.generated.types.unlock_args import V1


def test_unlock():
    args = {
        "unlock_args": V1(
            value={"authorization_data": AuthorizationData(payload=Payload(map=True))}
        )
    }

    accounts = {
        "authority": Pubkey.new_unique(),
        "token_owner": Pubkey.new_unique(),
        "token": Pubkey.new_unique(),
        "mint": Pubkey.new_unique(),
        "metadata": Pubkey.new_unique(),
        "edition": Pubkey.new_unique(),
        "token_record": Pubkey.new_unique(),
        "payer": Pubkey.new_unique(),
        "sysvar_instructions": Pubkey.new_unique(),
        "spl_token_program": Pubkey.new_unique(),
        "authorization_rules_program": Pubkey.new_unique(),
        "authorization_rules": Pubkey.new_unique(),
    }
    instruction = unlock(args, accounts)
    assert instruction.program_id == PROGRAM_ID
    assert len(instruction.accounts) == 13
    assert isinstance(instruction.data, bytes)


def test_unlock_with_remaining_accounts():
    args = {
        "unlock_args": V1(
            value={"authorization_data": AuthorizationData(payload=Payload(map=True))}
        )
    }
    accounts = {
        "authority": Pubkey.new_unique(),
        "token_owner": Pubkey.new_unique(),
        "token": Pubkey.new_unique(),
        "mint": Pubkey.new_unique(),
        "metadata": Pubkey.new_unique(),
        "edition": Pubkey.new_unique(),
        "token_record": Pubkey.new_unique(),
        "payer": Pubkey.new_unique(),
        "sysvar_instructions": Pubkey.new_unique(),
        "spl_token_program": Pubkey.new_unique(),
        "authorization_rules_program": Pubkey.new_unique(),
        "authorization_rules": Pubkey.new_unique(),
    }
    remaining_accounts = [
        AccountMeta(pubkey=Pubkey.new_unique(), is_signer=False, is_writable=False)
    ]
    instruction = unlock(args, accounts, remaining_accounts=remaining_accounts)
    assert len(instruction.accounts) == 13 + len(remaining_accounts)
