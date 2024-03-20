from solders.instruction import AccountMeta
from solders.pubkey import Pubkey

from original_metaplex_python.token_metadata.generated.instructions import (
    transfer_out_of_escrow,
)
from original_metaplex_python.token_metadata.generated.program_id import PROGRAM_ID
from original_metaplex_python.token_metadata.generated.types import (
    TransferOutOfEscrowArgs,
)


def test_transfer_out_of_escrow():
    args = {"transfer_out_of_escrow_args": TransferOutOfEscrowArgs(amount=1)}
    accounts = {
        "escrow": Pubkey.new_unique(),
        "metadata": Pubkey.new_unique(),
        "payer": Pubkey.new_unique(),
        "attribute_mint": Pubkey.new_unique(),
        "attribute_src": Pubkey.new_unique(),
        "attribute_dst": Pubkey.new_unique(),
        "escrow_mint": Pubkey.new_unique(),
        "escrow_account": Pubkey.new_unique(),
        "ata_program": Pubkey.new_unique(),
        "sysvar_instructions": Pubkey.new_unique(),
        "authority": Pubkey.new_unique(),
    }
    instruction = transfer_out_of_escrow(args, accounts)
    assert instruction.program_id == PROGRAM_ID
    assert len(instruction.accounts) == 13
    assert isinstance(instruction.data, bytes)


def test_transfer_out_of_escrow_with_remaining_accounts():
    args = {"transfer_out_of_escrow_args": TransferOutOfEscrowArgs(amount=1)}
    accounts = {
        "escrow": Pubkey.new_unique(),
        "metadata": Pubkey.new_unique(),
        "payer": Pubkey.new_unique(),
        "attribute_mint": Pubkey.new_unique(),
        "attribute_src": Pubkey.new_unique(),
        "attribute_dst": Pubkey.new_unique(),
        "escrow_mint": Pubkey.new_unique(),
        "escrow_account": Pubkey.new_unique(),
        "ata_program": Pubkey.new_unique(),
        "sysvar_instructions": Pubkey.new_unique(),
        "authority": Pubkey.new_unique(),
    }
    remaining_accounts = [
        AccountMeta(pubkey=Pubkey.new_unique(), is_signer=False, is_writable=False)
    ]
    instruction = transfer_out_of_escrow(
        args, accounts, remaining_accounts=remaining_accounts
    )
    assert len(instruction.accounts) == 14
