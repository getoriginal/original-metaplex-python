from solders.pubkey import Pubkey

from src.token_metadata.generated.types import (
    Uses,
    collection,
    collection_details,
    token_standard,
)
from src.token_metadata.generated.types.create_args import (
    V1,
    asset_data,
    from_decoded,
    from_json,
)
from src.token_metadata.generated.types.print_supply import Zero
from src.token_metadata.generated.types.token_standard import NonFungible
from src.token_metadata.generated.types.use_method import Single


def test_v1_to_json():
    asset_data_instance = asset_data.AssetData(
        name="Asset Name",
        symbol="SYM",
        uri="http://example.com",
        seller_fee_basis_points=500,
        creators=[],
        primary_sale_happened=False,
        is_mutable=True,
        token_standard=NonFungible(),
        collection=collection.Collection(verified=False, key=Pubkey.new_unique()),
        uses=Uses(use_method=Single, remaining=5, total=5),
        collection_details=collection_details.V1(value={"size": 5}),
        rule_set=Pubkey.new_unique(),
    )
    v1_instance = V1(
        value={"asset_data": asset_data_instance, "decimals": 8, "print_supply": Zero()}
    )
    json_data = v1_instance.to_json()
    expected = {
        "kind": "V1",
        "value": {
            "asset_data": asset_data_instance.to_json(),
            "decimals": 8,
            "print_supply": Zero().to_json(),
        },
    }
    assert json_data == expected


def test_v1_to_encodable():
    asset_data_instance = asset_data.AssetData(
        name="Asset Name",
        symbol="SYM",
        uri="http://example.com",
        seller_fee_basis_points=500,
        creators=[],
        primary_sale_happened=False,
        is_mutable=True,
        token_standard=NonFungible(),
        collection=collection.Collection(verified=False, key=Pubkey.new_unique()),
        uses=Uses(use_method=Single, remaining=5, total=5),
        collection_details=collection_details.V1(value={"size": 5}),
        rule_set=Pubkey.new_unique(),
    )

    v1_instance = V1(
        value={"asset_data": asset_data_instance, "decimals": 8, "print_supply": Zero()}
    )
    encodable = v1_instance.to_encodable()
    expected = {
        "V1": {
            "asset_data": asset_data_instance.to_encodable(),
            "decimals": 8,
            "print_supply": Zero().to_encodable(),
        },
    }
    assert encodable == expected


def test_from_decoded_v1():
    asset_data_instance = asset_data.AssetData(
        name="Asset Name",
        symbol="SYM",
        uri="http://example.com",
        seller_fee_basis_points=500,
        creators=[],
        primary_sale_happened=False,
        is_mutable=True,
        token_standard=NonFungible().to_encodable(),
        collection=collection.Collection(verified=False, key=Pubkey.new_unique()),
        uses=Uses(use_method=Single().to_encodable(), remaining=5, total=5),
        collection_details=collection_details.V1(value={"size": 5}).to_encodable(),
        rule_set=Pubkey.new_unique(),
    )

    decoded = {
        "V1": {
            "asset_data": asset_data_instance,
            "decimals": 8,
            "print_supply": Zero().to_encodable(),
        }
    }
    v1_instance = from_decoded(decoded)
    assert isinstance(v1_instance, V1)
    assert v1_instance.value["decimals"] == 8
    assert v1_instance.value["print_supply"] == Zero()


def test_from_json_v1():
    json_data = {
        "kind": "V1",
        "value": {
            "asset_data": {
                "name": "Asset Name",
                "symbol": "SYM",
                "uri": "http://example.com",
                "seller_fee_basis_points": 500,
                "creators": [],
                "primary_sale_happened": False,
                "is_mutable": True,
                "token_standard": token_standard.NonFungible().to_json(),
                "collection": {"verified": False, "key": str(Pubkey.new_unique())},
                "uses": Uses(use_method=Single(), remaining=5, total=5).to_json(),
                "collection_details": collection_details.V1(
                    value={"size": 5}
                ).to_json(),
                "rule_set": str(Pubkey.new_unique()),
            },
            "decimals": 8,
            "print_supply": Zero().to_json(),
        },
    }
    v1_instance = from_json(json_data)
    assert isinstance(v1_instance, V1)
    assert v1_instance.value["decimals"] == 8
    assert v1_instance.value["print_supply"], Zero()
