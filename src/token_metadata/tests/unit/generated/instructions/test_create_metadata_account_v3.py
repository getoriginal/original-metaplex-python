from solders.instruction import AccountMeta
from solders.pubkey import Pubkey

from src.token_metadata.generated.instructions import create_metadata_account_v3
from src.token_metadata.generated.types import CreateMetadataAccountArgsV3, DataV2


def test_create_metadata_account_v3():
    args = {
        "create_metadata_account_args_v3": CreateMetadataAccountArgsV3(
            data=DataV2(
                name="name",
                symbol="symbol",
                uri="uri",
                seller_fee_basis_points=10,
                creators=None,
                collection=None,
                uses=None,
            ),
            is_mutable=True,
            collection_details=None,
        )
    }
    accounts = {
        "metadata": Pubkey.new_unique(),
        "mint": Pubkey.new_unique(),
        "mint_authority": Pubkey.new_unique(),
        "payer": Pubkey.new_unique(),
        "update_authority": Pubkey.new_unique(),
    }
    instruction = create_metadata_account_v3(args, accounts)
    assert len(instruction.accounts) == 7
    assert isinstance(instruction.data, bytes)


def test_create_metadata_account_v3_with_remaining_accounts():
    args = {
        "create_metadata_account_args_v3": CreateMetadataAccountArgsV3(
            data=DataV2(
                name="name",
                symbol="symbol",
                uri="uri",
                seller_fee_basis_points=10,
                creators=None,
                collection=None,
                uses=None,
            ),
            is_mutable=True,
            collection_details=None,
        )
    }
    accounts = {
        "metadata": Pubkey.new_unique(),
        "mint": Pubkey.new_unique(),
        "mint_authority": Pubkey.new_unique(),
        "payer": Pubkey.new_unique(),
        "update_authority": Pubkey.new_unique(),
    }
    remaining_accounts = [
        AccountMeta(pubkey=Pubkey.new_unique(), is_signer=False, is_writable=False)
    ]
    instruction = create_metadata_account_v3(
        args, accounts, remaining_accounts=remaining_accounts
    )
    assert len(instruction.accounts) == 8
