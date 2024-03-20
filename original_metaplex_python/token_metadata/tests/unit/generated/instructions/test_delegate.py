from solders.instruction import AccountMeta
from solders.pubkey import Pubkey

from original_metaplex_python.token_metadata.generated.instructions import delegate
from original_metaplex_python.token_metadata.generated.program_id import PROGRAM_ID
from original_metaplex_python.token_metadata.generated.types import (
    AuthorizationData,
    Payload,
)
from original_metaplex_python.token_metadata.generated.types.delegate_args import (
    CollectionV1,
)


def test_delegate():
    args = {
        "delegate_args": CollectionV1(
            value={"authorization_data": AuthorizationData(payload=Payload(map=True))}
        )
    }
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
    instruction = delegate(args, accounts)
    assert instruction.program_id == PROGRAM_ID
    assert len(instruction.accounts) == 14
    assert isinstance(instruction.data, bytes)


def test_delegate_with_remaining_accounts():
    args = {
        "delegate_args": CollectionV1(
            value={"authorization_data": AuthorizationData(payload=Payload(map=True))}
        )
    }
    accounts = {
        "delegate_record": Pubkey.new_unique(),
        "delegate": Pubkey.new_unique(),
        "metadata": Pubkey.new_unique(),
        "master_edition": None,
        "token_record": None,
        "mint": Pubkey.new_unique(),
        "token": None,
        "authority": Pubkey.new_unique(),
        "payer": Pubkey.new_unique(),
        "sysvar_instructions": Pubkey.new_unique(),
        "spl_token_program": None,
        "authorization_rules_program": None,
        "authorization_rules": None,
    }
    remaining_accounts = [
        AccountMeta(pubkey=Pubkey.new_unique(), is_signer=False, is_writable=False)
    ]
    instruction = delegate(args, accounts, remaining_accounts=remaining_accounts)
    assert len(instruction.accounts) == 15
