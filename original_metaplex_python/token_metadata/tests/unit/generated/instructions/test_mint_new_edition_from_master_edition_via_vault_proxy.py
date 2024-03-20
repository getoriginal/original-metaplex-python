from solders.instruction import AccountMeta
from solders.pubkey import Pubkey

from original_metaplex_python.token_metadata.generated.instructions import (
    mint_new_edition_from_master_edition_via_vault_proxy,
)
from original_metaplex_python.token_metadata.generated.program_id import PROGRAM_ID
from original_metaplex_python.token_metadata.generated.types import (
    MintNewEditionFromMasterEditionViaTokenArgs,
)


def test_mint_new_edition_from_master_edition_via_vault_proxy():
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
        "vault_authority": Pubkey.new_unique(),
        "safety_deposit_store": Pubkey.new_unique(),
        "safety_deposit_box": Pubkey.new_unique(),
        "vault": Pubkey.new_unique(),
        "new_metadata_update_authority": Pubkey.new_unique(),
        "metadata": Pubkey.new_unique(),
        "token_vault_program": Pubkey.new_unique(),
    }
    instruction = mint_new_edition_from_master_edition_via_vault_proxy(args, accounts)
    assert instruction.program_id == PROGRAM_ID
    assert len(instruction.accounts) == 17
    assert isinstance(instruction.data, bytes)


def test_mint_new_edition_from_master_edition_via_vault_proxy_with_remaining_accounts():
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
        "vault_authority": Pubkey.new_unique(),
        "safety_deposit_store": Pubkey.new_unique(),
        "safety_deposit_box": Pubkey.new_unique(),
        "vault": Pubkey.new_unique(),
        "new_metadata_update_authority": Pubkey.new_unique(),
        "metadata": Pubkey.new_unique(),
        "token_vault_program": Pubkey.new_unique(),
    }
    remaining_accounts = [
        AccountMeta(pubkey=Pubkey.new_unique(), is_signer=False, is_writable=False)
    ]
    instruction = mint_new_edition_from_master_edition_via_vault_proxy(
        args, accounts, remaining_accounts=remaining_accounts
    )
    assert len(instruction.accounts) == 18
