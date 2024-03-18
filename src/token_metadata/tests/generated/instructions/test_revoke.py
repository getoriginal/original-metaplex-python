from solders.instruction import AccountMeta
from solders.pubkey import Pubkey

from src.token_metadata.generated.instructions import revoke
from src.token_metadata.generated.program_id import PROGRAM_ID
from src.token_metadata.generated.types.revoke_args import CollectionV1


def test_revoke():
    args = {"revoke_args": CollectionV1()}
    accounts = {
        "delegate_record": Pubkey.new_unique(),
        "delegate": Pubkey.new_unique(),
        "metadata": Pubkey.new_unique(),
        "master_edition": Pubkey.new_unique(),
        "token_record": Pubkey.new_unique(),
        "mint": Pubkey.new_unique(),
        "token": Pubkey.new_unique(),
        "authority": Pubkey.new_unique(),
        "payer": Pubkey.new_unique(),
        "sysvar_instructions": Pubkey.new_unique(),
        "spl_token_program": Pubkey.new_unique(),
        "authorization_rules_program": Pubkey.new_unique(),
        "authorization_rules": Pubkey.new_unique(),
    }
    instruction = revoke(args, accounts)
    assert instruction.program_id == PROGRAM_ID
    assert len(instruction.accounts) == 14
    assert isinstance(instruction.data, bytes)


def test_revoke_with_remaining_accounts():
    args = {"revoke_args": CollectionV1()}
    accounts = {
        "delegate_record": None,  # Optional field set to None
        "delegate": Pubkey.new_unique(),
        "metadata": Pubkey.new_unique(),
        "master_edition": None,  # Optional field set to None
        "token_record": None,  # Optional field set to None
        "mint": Pubkey.new_unique(),
        "token": None,  # Optional field set to None
        "authority": Pubkey.new_unique(),
        "payer": Pubkey.new_unique(),
        "sysvar_instructions": Pubkey.new_unique(),
        "spl_token_program": None,  # Optional field set to None
        "authorization_rules_program": None,  # Optional field set to None
        "authorization_rules": None,  # Optional field set to None
    }
    remaining_accounts = [
        AccountMeta(pubkey=Pubkey.new_unique(), is_signer=False, is_writable=False)
    ]
    instruction = revoke(args, accounts, remaining_accounts=remaining_accounts)
    assert len(instruction.accounts) == 15
