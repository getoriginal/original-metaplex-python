from solders.instruction import AccountMeta
from solders.pubkey import Pubkey

from src.token_metadata.generated.instructions import print
from src.token_metadata.generated.program_id import PROGRAM_ID
from src.token_metadata.generated.types.print_args import PrintArgsKind


def test_print():
    args = {
        "print_args": PrintArgsKind(
            value={
                "edition": 1,
            }
        )
    }
    accounts = {
        "edition_metadata": Pubkey.new_unique(),
        "edition": Pubkey.new_unique(),
        "edition_mint": Pubkey.new_unique(),
        "edition_token_account_owner": Pubkey.new_unique(),
        "edition_token_account": Pubkey.new_unique(),
        "edition_mint_authority": Pubkey.new_unique(),
        "edition_token_record": Pubkey.new_unique(),
        "master_edition": Pubkey.new_unique(),
        "edition_marker_pda": Pubkey.new_unique(),
        "payer": Pubkey.new_unique(),
        "master_token_account_owner": Pubkey.new_unique(),
        "master_token_account": Pubkey.new_unique(),
        "master_metadata": Pubkey.new_unique(),
        "update_authority": Pubkey.new_unique(),
        "spl_token_program": Pubkey.new_unique(),
        "spl_ata_program": Pubkey.new_unique(),
        "sysvar_instructions": Pubkey.new_unique(),
    }
    instruction = print(args, accounts)
    assert instruction.program_id == PROGRAM_ID
    assert len(instruction.accounts) == 18
    assert isinstance(instruction.data, bytes)


def test_print_with_remaining_accounts():
    args = {
        "print_args": PrintArgsKind(
            value={
                "edition": 1,
            }
        )
    }
    accounts = {
        "edition_metadata": Pubkey.new_unique(),
        "edition": Pubkey.new_unique(),
        "edition_mint": Pubkey.new_unique(),
        "edition_token_account_owner": Pubkey.new_unique(),
        "edition_token_account": Pubkey.new_unique(),
        "edition_mint_authority": Pubkey.new_unique(),
        "edition_token_record": Pubkey.new_unique(),
        "master_edition": Pubkey.new_unique(),
        "edition_marker_pda": Pubkey.new_unique(),
        "payer": Pubkey.new_unique(),
        "master_token_account_owner": Pubkey.new_unique(),
        "master_token_account": Pubkey.new_unique(),
        "master_metadata": Pubkey.new_unique(),
        "update_authority": Pubkey.new_unique(),
        "spl_token_program": Pubkey.new_unique(),
        "spl_ata_program": Pubkey.new_unique(),
        "sysvar_instructions": Pubkey.new_unique(),
    }
    remaining_accounts = [
        AccountMeta(pubkey=Pubkey.new_unique(), is_signer=False, is_writable=False)
    ]
    instruction = print(args, accounts, remaining_accounts=remaining_accounts)
    assert len(instruction.accounts) == 19
