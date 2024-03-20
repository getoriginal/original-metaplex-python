from solders.instruction import AccountMeta
from solders.pubkey import Pubkey

from original_metaplex_python.token_metadata.generated.instructions.create import create
from original_metaplex_python.token_metadata.generated.program_id import PROGRAM_ID
from original_metaplex_python.token_metadata.generated.types import AssetData
from original_metaplex_python.token_metadata.generated.types.create_args import (
    V1,
    V1Value,
)
from original_metaplex_python.token_metadata.generated.types.token_standard import (
    NonFungible,
)


def mock_create_args():
    return V1(
        value=V1Value(
            asset_data=AssetData(
                name="name",
                symbol="symbol",
                uri="uri",
                seller_fee_basis_points=42,
                creators=[],
                primary_sale_happened=False,
                is_mutable=True,
                token_standard=NonFungible(),
                collection=None,
                uses=None,
                collection_details=None,
                rule_set=None,
            ),
            decimals=0,
            print_supply=None,
        )
    )


def test_create_basic():
    metadata = Pubkey.new_unique()
    master_edition = Pubkey.new_unique()
    mint = Pubkey.new_unique()
    authority = Pubkey.new_unique()
    payer = Pubkey.new_unique()
    update_authority = Pubkey.new_unique()
    sysvar_instructions = Pubkey.new_unique()
    spl_token_program = Pubkey.new_unique()

    args = {"create_args": mock_create_args()}

    instruction = create(
        args=args,
        accounts={
            "metadata": metadata,
            "master_edition": master_edition,
            "mint": mint,
            "authority": authority,
            "payer": payer,
            "update_authority": update_authority,
            "sysvar_instructions": sysvar_instructions,
            "spl_token_program": spl_token_program,
        },
        program_id=PROGRAM_ID,
    )

    assert instruction.program_id == PROGRAM_ID
    assert len(instruction.accounts) == 9
    assert instruction.accounts[0].pubkey == metadata
    assert instruction.data.startswith(bytes([42]))


def test_create_with_remaining_accounts():
    additional_account = AccountMeta(
        pubkey=Pubkey.new_unique(), is_signer=False, is_writable=False
    )

    instruction = create(
        args={"create_args": mock_create_args()},
        accounts={
            "metadata": Pubkey.new_unique(),
            "master_edition": Pubkey.new_unique(),
            "mint": Pubkey.new_unique(),
            "authority": Pubkey.new_unique(),
            "payer": Pubkey.new_unique(),
            "update_authority": Pubkey.new_unique(),
            "sysvar_instructions": Pubkey.new_unique(),
            "spl_token_program": Pubkey.new_unique(),
        },
        program_id=PROGRAM_ID,
        remaining_accounts=[additional_account],
    )

    assert len(instruction.accounts) == 10
    assert instruction.accounts[-1].pubkey == additional_account.pubkey
