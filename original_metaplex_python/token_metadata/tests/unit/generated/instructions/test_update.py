from solders.instruction import AccountMeta
from solders.pubkey import Pubkey

from original_metaplex_python.token_metadata.generated.instructions import update
from original_metaplex_python.token_metadata.generated.program_id import PROGRAM_ID
from original_metaplex_python.token_metadata.generated.types import (
    AuthorizationData,
    Payload,
)
from original_metaplex_python.token_metadata.generated.types.collection_details_toggle import (
    None_ as CollectionDetailsToggleNone,
)
from original_metaplex_python.token_metadata.generated.types.collection_toggle import (
    None_ as CollectionToggleNone,
)
from original_metaplex_python.token_metadata.generated.types.rule_set_toggle import (
    None_ as RuleSetNone,
)
from original_metaplex_python.token_metadata.generated.types.update_args import V1
from original_metaplex_python.token_metadata.generated.types.uses_toggle import None_


def test_update():
    args = {
        "update_args": V1(
            value={
                "new_update_authority": Pubkey.new_unique(),
                "data": None,
                "primary_sale_happened": False,
                "is_mutable": False,
                "collection": CollectionToggleNone(),
                "collection_details": CollectionDetailsToggleNone(),
                "uses": None_(),
                "rule_set": RuleSetNone(),
                "authorization_data": AuthorizationData(payload=Payload(map=True)),
            }
        )
    }
    accounts = {
        "authority": Pubkey.new_unique(),
        "delegate_record": Pubkey.new_unique(),
        "token": Pubkey.new_unique(),
        "mint": Pubkey.new_unique(),
        "metadata": Pubkey.new_unique(),
        "edition": Pubkey.new_unique(),
        "payer": Pubkey.new_unique(),
        "sysvar_instructions": Pubkey.new_unique(),
        "authorization_rules_program": Pubkey.new_unique(),
        "authorization_rules": Pubkey.new_unique(),
    }
    instruction = update(args, accounts)
    assert instruction.program_id == PROGRAM_ID
    assert len(instruction.accounts) == 11
    assert isinstance(instruction.data, bytes)


def test_update_with_remaining_accounts():
    args = {
        "update_args": V1(
            value={
                "new_update_authority": Pubkey.new_unique(),
                "data": None,
                "primary_sale_happened": False,
                "is_mutable": False,
                "collection": CollectionToggleNone(),
                "collection_details": CollectionDetailsToggleNone(),
                "uses": None_(),
                "rule_set": RuleSetNone(),
                "authorization_data": AuthorizationData(payload=Payload(map=True)),
            }
        )
    }
    accounts = {
        "authority": Pubkey.new_unique(),
        "delegate_record": Pubkey.new_unique(),
        "token": Pubkey.new_unique(),
        "mint": Pubkey.new_unique(),
        "metadata": Pubkey.new_unique(),
        "edition": Pubkey.new_unique(),
        "payer": Pubkey.new_unique(),
        "sysvar_instructions": Pubkey.new_unique(),
        "authorization_rules_program": Pubkey.new_unique(),
        "authorization_rules": Pubkey.new_unique(),
    }
    remaining_accounts = [
        AccountMeta(pubkey=Pubkey.new_unique(), is_signer=False, is_writable=False)
    ]
    instruction = update(args, accounts, remaining_accounts=remaining_accounts)
    assert len(instruction.accounts) == 11 + len(remaining_accounts)
