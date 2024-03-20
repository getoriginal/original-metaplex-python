from solders.instruction import AccountMeta
from solders.pubkey import Pubkey

from src.token_metadata.generated.instructions import transfer
from src.token_metadata.generated.program_id import PROGRAM_ID
from src.token_metadata.generated.types import (
    AuthorizationData,
    Payload,
    TransferArgsKind,
)


def test_transfer():
    args = {
        "transfer_args": TransferArgsKind(
            value={
                "amount": 1,
                "authorization_data": AuthorizationData(payload=Payload(map=True)),
            }
        )
    }
    accounts = {
        "token": Pubkey.new_unique(),
        "token_owner": Pubkey.new_unique(),
        "destination": Pubkey.new_unique(),
        "destination_owner": Pubkey.new_unique(),
        "mint": Pubkey.new_unique(),
        "metadata": Pubkey.new_unique(),
        "edition": Pubkey.new_unique(),
        "owner_token_record": Pubkey.new_unique(),
        "destination_token_record": Pubkey.new_unique(),
        "authority": Pubkey.new_unique(),
        "payer": Pubkey.new_unique(),
        "sysvar_instructions": Pubkey.new_unique(),
        "spl_token_program": Pubkey.new_unique(),
        "spl_ata_program": Pubkey.new_unique(),
        "authorization_rules_program": Pubkey.new_unique(),
        "authorization_rules": Pubkey.new_unique(),
    }
    instruction = transfer(args, accounts)
    assert instruction.program_id == PROGRAM_ID
    assert len(instruction.accounts) == 17
    assert isinstance(instruction.data, bytes)


def test_transfer_with_remaining_accounts():
    args = {
        "transfer_args": TransferArgsKind(
            value={
                "amount": 1,
                "authorization_data": AuthorizationData(payload=Payload(map=True)),
            }
        )
    }
    accounts = {
        "token": Pubkey.new_unique(),
        "token_owner": Pubkey.new_unique(),
        "destination": Pubkey.new_unique(),
        "destination_owner": Pubkey.new_unique(),
        "mint": Pubkey.new_unique(),
        "metadata": Pubkey.new_unique(),
        "edition": Pubkey.new_unique(),
        "owner_token_record": Pubkey.new_unique(),
        "destination_token_record": Pubkey.new_unique(),
        "authority": Pubkey.new_unique(),
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
    instruction = transfer(args, accounts, remaining_accounts=remaining_accounts)
    assert len(instruction.accounts) == 15 + len(remaining_accounts) + len(
        [
            accounts[key]
            for key in ["authorization_rules_program", "authorization_rules"]
            if accounts.get(key)
        ]
    )
