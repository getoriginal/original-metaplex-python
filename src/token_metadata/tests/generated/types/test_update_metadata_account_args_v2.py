from construct import Container
from solders.pubkey import Pubkey

from src.token_metadata.generated.types import Collection, Uses
from src.token_metadata.generated.types.data_v2 import DataV2
from src.token_metadata.generated.types.update_metadata_account_args_v2 import (
    UpdateMetadataAccountArgsV2,
)
from src.token_metadata.generated.types.use_method import Single

data_example = DataV2(
    name="Example",
    symbol="EX",
    uri="http://example.com",
    seller_fee_basis_points=1000,
    creators=[],
    collection=Collection(verified=True, key=Pubkey.new_unique()),
    uses=Uses(use_method=Single(), remaining=10, total=100),
)


def test_update_metadata_account_args_v2_to_encodable():
    update_authority = Pubkey.new_unique()
    primary_sale_happened = True
    is_mutable = True
    args = UpdateMetadataAccountArgsV2(
        data=data_example,
        update_authority=update_authority,
        primary_sale_happened=primary_sale_happened,
        is_mutable=is_mutable,
    )
    encodable = args.to_encodable()
    assert encodable == {
        "data": data_example.to_encodable(),
        "update_authority": update_authority,
        "primary_sale_happened": primary_sale_happened,
        "is_mutable": is_mutable,
    }


def test_update_metadata_account_args_v2_from_decoded():
    update_authority = Pubkey.new_unique()
    primary_sale_happened = True
    is_mutable = True
    decoded_data = DataV2(
        name="Example",
        symbol="EX",
        uri="http://example.com",
        seller_fee_basis_points=1000,
        creators=[],
        collection=Collection(verified=True, key=Pubkey.new_unique()),
        uses=Uses(use_method=Single.to_encodable(), remaining=10, total=100),
    )
    decoded = Container(
        data=decoded_data,
        update_authority=update_authority,
        primary_sale_happened=primary_sale_happened,
        is_mutable=is_mutable,
    )
    args = UpdateMetadataAccountArgsV2.from_decoded(decoded)

    assert args.data.name == decoded_data.name
    assert args.update_authority == update_authority
    assert args.primary_sale_happened == primary_sale_happened
    assert args.is_mutable == is_mutable


def test_update_metadata_account_args_v2_to_json():
    update_authority = Pubkey.new_unique()
    primary_sale_happened = True
    is_mutable = True
    args = UpdateMetadataAccountArgsV2(
        data=data_example,
        update_authority=update_authority,
        primary_sale_happened=primary_sale_happened,
        is_mutable=is_mutable,
    )
    json_obj = args.to_json()
    assert json_obj == {
        "data": data_example.to_json(),
        "update_authority": str(update_authority),
        "primary_sale_happened": primary_sale_happened,
        "is_mutable": is_mutable,
    }


def test_update_metadata_account_args_v2_from_json():
    update_authority_str = str(Pubkey.new_unique())
    primary_sale_happened = True
    is_mutable = True
    json_obj = {
        "data": data_example.to_json(),
        "update_authority": update_authority_str,
        "primary_sale_happened": primary_sale_happened,
        "is_mutable": is_mutable,
    }
    args = UpdateMetadataAccountArgsV2.from_json(json_obj)
    assert (
        isinstance(args, UpdateMetadataAccountArgsV2)
        and str(args.update_authority) == update_authority_str
        and args.primary_sale_happened == primary_sale_happened
        and args.is_mutable == is_mutable
    )
