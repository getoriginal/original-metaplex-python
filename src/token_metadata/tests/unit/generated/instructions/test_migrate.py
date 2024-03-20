from solders.instruction import AccountMeta
from solders.pubkey import Pubkey

from src.token_metadata.generated.instructions import migrate
from src.token_metadata.generated.program_id import PROGRAM_ID


def test_migrate():
    accounts = {
        "metadata": Pubkey.new_unique(),
        "edition": Pubkey.new_unique(),
        "token": Pubkey.new_unique(),
        "token_owner": Pubkey.new_unique(),
        "mint": Pubkey.new_unique(),
        "payer": Pubkey.new_unique(),
        "authority": Pubkey.new_unique(),
        "collection_metadata": Pubkey.new_unique(),
        "delegate_record": Pubkey.new_unique(),
        "token_record": Pubkey.new_unique(),
        "sysvar_instructions": Pubkey.new_unique(),
        "spl_token_program": Pubkey.new_unique(),
        "authorization_rules_program": Pubkey.new_unique(),
        "authorization_rules": Pubkey.new_unique(),
    }
    instruction = migrate(accounts)
    assert instruction.program_id == PROGRAM_ID
    assert len(instruction.accounts) == 15
    assert isinstance(instruction.data, bytes)


def test_migrate_with_remaining_accounts():
    accounts = {
        "metadata": Pubkey.new_unique(),
        "edition": Pubkey.new_unique(),
        "token": Pubkey.new_unique(),
        "token_owner": Pubkey.new_unique(),
        "mint": Pubkey.new_unique(),
        "payer": Pubkey.new_unique(),
        "authority": Pubkey.new_unique(),
        "collection_metadata": Pubkey.new_unique(),
        "delegate_record": Pubkey.new_unique(),
        "token_record": Pubkey.new_unique(),
        "sysvar_instructions": Pubkey.new_unique(),
        "spl_token_program": Pubkey.new_unique(),
        "authorization_rules_program": Pubkey.new_unique(),
        "authorization_rules": Pubkey.new_unique(),
    }
    remaining_accounts = [
        AccountMeta(pubkey=Pubkey.new_unique(), is_signer=False, is_writable=False)
    ]
    instruction = migrate(accounts, remaining_accounts=remaining_accounts)
    assert len(instruction.accounts) == 16
