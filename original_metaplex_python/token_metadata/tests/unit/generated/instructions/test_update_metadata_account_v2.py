from solders.instruction import AccountMeta
from solders.pubkey import Pubkey

from original_metaplex_python.token_metadata.generated.instructions import (
    update_metadata_account_v2,
)
from original_metaplex_python.token_metadata.generated.program_id import PROGRAM_ID
from original_metaplex_python.token_metadata.generated.types import (
    update_metadata_account_args_v2 as args_types,
)


def test_update_metadata_account_v2():
    args = {
        "update_metadata_account_args_v2": args_types.UpdateMetadataAccountArgsV2(
            data=None,
            update_authority=Pubkey.new_unique(),
            primary_sale_happened=False,
            is_mutable=False,
        )
    }
    accounts = {
        "metadata": Pubkey.new_unique(),
        "update_authority": Pubkey.new_unique(),
    }
    instruction = update_metadata_account_v2(args, accounts)
    assert instruction.program_id == PROGRAM_ID
    assert len(instruction.accounts) == 2
    assert isinstance(instruction.data, bytes)


def test_update_metadata_account_v2_with_remaining_accounts():
    args = {
        "update_metadata_account_args_v2": args_types.UpdateMetadataAccountArgsV2(
            data=None,
            update_authority=Pubkey.new_unique(),
            primary_sale_happened=False,
            is_mutable=False,
        )
    }
    accounts = {
        "metadata": Pubkey.new_unique(),
        "update_authority": Pubkey.new_unique(),
    }
    remaining_accounts = [
        AccountMeta(pubkey=Pubkey.new_unique(), is_signer=False, is_writable=False)
    ]
    instruction = update_metadata_account_v2(
        args, accounts, remaining_accounts=remaining_accounts
    )
    assert len(instruction.accounts) == 2 + len(remaining_accounts)
