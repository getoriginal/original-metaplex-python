from solders.instruction import AccountMeta
from solders.pubkey import Pubkey

from src.token_metadata.generated.instructions import (
    mint_new_edition_from_master_edition_via_token,
)
from src.token_metadata.generated.program_id import PROGRAM_ID
from src.token_metadata.generated.types.mint_new_edition_from_master_edition_via_token_args import (
    MintNewEditionFromMasterEditionViaTokenArgs,
)


def test_mint_new_edition_from_master_edition_via_token():
    args = {
        "mint_new_edition_from_master_edition_via_token_args": MintNewEditionFromMasterEditionViaTokenArgs(
            edition=1
        )
    }
    accounts = {
        "new_metadata": Pubkey.new_unique(),
        "new_edition": Pubkey.new_unique(),
        "master_edition": Pubkey.new_unique(),
        "new_mint": Pubkey.new_unique(),
        "edition_mark_pda": Pubkey.new_unique(),
        "new_mint_authority": Pubkey.new_unique(),
        "payer": Pubkey.new_unique(),
        "token_account_owner": Pubkey.new_unique(),
        "token_account": Pubkey.new_unique(),
        "new_metadata_update_authority": Pubkey.new_unique(),
        "metadata": Pubkey.new_unique(),
    }
    instruction = mint_new_edition_from_master_edition_via_token(args, accounts)
    assert instruction.program_id == PROGRAM_ID
    assert len(instruction.accounts) == 14
    assert isinstance(instruction.data, bytes)


def test_mint_new_edition_from_master_edition_via_token_with_remaining_accounts():
    args = {
        "mint_new_edition_from_master_edition_via_token_args": MintNewEditionFromMasterEditionViaTokenArgs(
            edition=1
        )
    }
    accounts = {
        "new_metadata": Pubkey.new_unique(),
        "new_edition": Pubkey.new_unique(),
        "master_edition": Pubkey.new_unique(),
        "new_mint": Pubkey.new_unique(),
        "edition_mark_pda": Pubkey.new_unique(),
        "new_mint_authority": Pubkey.new_unique(),
        "payer": Pubkey.new_unique(),
        "token_account_owner": Pubkey.new_unique(),
        "token_account": Pubkey.new_unique(),
        "new_metadata_update_authority": Pubkey.new_unique(),
        "metadata": Pubkey.new_unique(),
    }
    remaining_accounts = [
        AccountMeta(pubkey=Pubkey.new_unique(), is_signer=False, is_writable=False)
    ]
    instruction = mint_new_edition_from_master_edition_via_token(
        args, accounts, remaining_accounts=remaining_accounts
    )
    assert len(instruction.accounts) == 15