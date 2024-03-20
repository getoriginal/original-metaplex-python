from solders.instruction import AccountMeta
from solders.pubkey import Pubkey

from original_metaplex_python.token_metadata.generated.instructions import mint
from original_metaplex_python.token_metadata.generated.program_id import PROGRAM_ID
from original_metaplex_python.token_metadata.generated.types import (
    AuthorizationData,
    Payload,
)
from original_metaplex_python.token_metadata.generated.types.mint_args import (
    MintArgsKind,
)


def test_mint():
    args = {
        "mint_args": MintArgsKind(
            value={
                "amount": 1,
                "authorization_data": AuthorizationData(payload=Payload(map=True)),
            }
        )
    }
    accounts = {
        "token": Pubkey.new_unique(),
        "token_owner": Pubkey.new_unique(),
        "metadata": Pubkey.new_unique(),
        "master_edition": Pubkey.new_unique(),
        "token_record": Pubkey.new_unique(),
        "mint": Pubkey.new_unique(),
        "authority": Pubkey.new_unique(),
        "delegate_record": Pubkey.new_unique(),
        "payer": Pubkey.new_unique(),
        "sysvar_instructions": Pubkey.new_unique(),
        "spl_token_program": Pubkey.new_unique(),
        "spl_ata_program": Pubkey.new_unique(),
        "authorization_rules_program": Pubkey.new_unique(),
        "authorization_rules": Pubkey.new_unique(),
    }
    instruction = mint(args, accounts)
    assert instruction.program_id == PROGRAM_ID
    assert len(instruction.accounts) == 15
    assert isinstance(instruction.data, bytes)


def test_mint_with_remaining_accounts():
    args = {
        "mint_args": MintArgsKind(
            value={
                "amount": 1,
                "authorization_data": AuthorizationData(payload=Payload(map=True)),
            }
        )
    }
    accounts = {
        "token": Pubkey.new_unique(),
        "token_owner": Pubkey.new_unique(),
        "metadata": Pubkey.new_unique(),
        "master_edition": Pubkey.new_unique(),
        "token_record": Pubkey.new_unique(),
        "mint": Pubkey.new_unique(),
        "authority": Pubkey.new_unique(),
        "delegate_record": Pubkey.new_unique(),
        "payer": Pubkey.new_unique(),
        "sysvar_instructions": Pubkey.new_unique(),
        "spl_token_program": Pubkey.new_unique(),
        "spl_ata_program": Pubkey.new_unique(),
        "authorization_rules_program": Pubkey.new_unique(),
        "authorization_rules": Pubkey.new_unique(),
    }
    remaining_accounts = [
        AccountMeta(pubkey=Pubkey.new_unique(), is_signer=False, is_writable=False)
    ]
    instruction = mint(args, accounts, remaining_accounts=remaining_accounts)
    assert len(instruction.accounts) == 16
