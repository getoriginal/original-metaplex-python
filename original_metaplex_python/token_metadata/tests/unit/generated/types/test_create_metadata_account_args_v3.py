from solders.pubkey import Pubkey

from original_metaplex_python.token_metadata.generated.types import (
    DataV2,
    Uses,
    collection,
    creator,
    uses,
)
from original_metaplex_python.token_metadata.generated.types.collection_details import (
    V1,
)
from original_metaplex_python.token_metadata.generated.types.create_metadata_account_args_v3 import (
    CreateMetadataAccountArgsV3,
)
from original_metaplex_python.token_metadata.generated.types.use_method import Single


def test_create_metadata_account_args_v3_to_json():
    data_instance = DataV2(
        name="Test Asset",
        symbol="TST",
        uri="https://example.com/asset",
        seller_fee_basis_points=500,
        creators=[
            creator.Creator(address=Pubkey.new_unique(), verified=True, share=100)
        ],
        collection=collection.Collection(verified=True, key=Pubkey.new_unique()),
        uses=uses.Uses(use_method=Single, remaining=1, total=1),
    )
    collection_details_instance = V1(value={"size": 10})
    args = CreateMetadataAccountArgsV3(
        data=data_instance,
        is_mutable=True,
        collection_details=collection_details_instance,
    )
    json_data = args.to_json()
    assert json_data["is_mutable"] is True
    assert json_data["data"]["name"] == "Test Asset"
    assert json_data["collection_details"]["kind"] == "V1"


def test_create_metadata_account_args_v3_from_json():
    json_data = {
        "data": {
            "name": "Test Asset",
            "symbol": "TST",
            "uri": "https://example.com/asset",
            "seller_fee_basis_points": 500,
            "creators": [
                {"address": str(Pubkey.new_unique()), "verified": True, "share": 100}
            ],
            "collection": {"verified": True, "key": str(Pubkey.new_unique())},
            "uses": Uses(use_method=Single(), remaining=5, total=5).to_json(),
        },
        "is_mutable": True,
        "collection_details": {"kind": "V1", "value": {"size": 10}},
    }
    args = CreateMetadataAccountArgsV3.from_json(json_data)
    assert args.is_mutable is True
    assert args.data.name == "Test Asset"
    assert isinstance(args.collection_details, V1)


def test_create_metadata_account_args_v3_to_encodable():
    data_instance = DataV2(
        name="Test Asset",
        symbol="TST",
        uri="https://example.com/asset",
        seller_fee_basis_points=500,
        creators=[
            creator.Creator(address=Pubkey.new_unique(), verified=True, share=100)
        ],
        collection=collection.Collection(verified=True, key=Pubkey.new_unique()),
        uses=uses.Uses(use_method=Single, remaining=1, total=1),
    )
    collection_details_instance = V1(value={"size": 10})
    args = CreateMetadataAccountArgsV3(
        data=data_instance,
        is_mutable=True,
        collection_details=collection_details_instance,
    )
    encodable = args.to_encodable()
    assert encodable["is_mutable"] is True
    assert encodable["data"]["name"] == "Test Asset"
    assert "V1" in encodable["collection_details"]


def test_create_metadata_account_args_v3_from_decoded():
    data_instance = DataV2(
        name="Test Asset",
        symbol="TST",
        uri="https://example.com/asset",
        seller_fee_basis_points=500,
        creators=[
            creator.Creator(address=Pubkey.new_unique(), verified=True, share=100)
        ],
        collection=collection.Collection(verified=True, key=Pubkey.new_unique()),
        uses=uses.Uses(use_method=Single().to_encodable(), remaining=1, total=1),
    )
    collection_details_instance = V1(value={"size": 10}).to_encodable()
    args = CreateMetadataAccountArgsV3(
        data=data_instance,
        is_mutable=True,
        collection_details=collection_details_instance,
    )

    args = CreateMetadataAccountArgsV3.from_decoded(args)
    assert args.is_mutable is True
    assert args.data.name == "Test Asset"
    assert isinstance(args.collection_details, V1)
