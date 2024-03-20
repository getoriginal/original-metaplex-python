from dataclasses import asdict

from construct import Container
from solders.pubkey import Pubkey

from original_metaplex_python.token_metadata.generated.types import (
    AssetData,
    Uses,
    collection,
    collection_details,
    creator,
    token_standard,
)
from original_metaplex_python.token_metadata.generated.types.collection_details import (
    V1,
)
from original_metaplex_python.token_metadata.generated.types.token_standard import (
    NonFungible,
)
from original_metaplex_python.token_metadata.generated.types.use_method import Single


def test_asset_data_to_encodable():
    args = AssetData(
        name="Example Name",
        symbol="EXM",
        uri="https://example.com",
        seller_fee_basis_points=500,
        creators=[
            creator.Creator(address=Pubkey.new_unique(), verified=False, share=100)
        ],
        primary_sale_happened=False,
        is_mutable=True,
        token_standard=NonFungible(),
        collection=collection.Collection(verified=False, key=Pubkey.new_unique()),
        uses=Uses(use_method=Single, remaining=5, total=5),
        collection_details=collection_details.V1(value={"size": 5}),
        rule_set=Pubkey.new_unique(),
    )
    encodable = args.to_encodable()

    expected_data = {
        "name": args.name,
        "symbol": args.symbol,
        "uri": args.uri,
        "seller_fee_basis_points": args.seller_fee_basis_points,
        "creators": [asdict(creator) for creator in args.creators],
        "primary_sale_happened": args.primary_sale_happened,
        "is_mutable": args.is_mutable,
        "token_standard": args.token_standard.to_encodable(),
        "collection": args.collection.to_encodable(),
        "uses": args.uses.to_encodable(),
        "collection_details": args.collection_details.to_encodable(),
        "rule_set": args.rule_set,
    }
    assert encodable["name"] == expected_data["name"]
    assert encodable["symbol"] == expected_data["symbol"]
    assert encodable["uri"] == expected_data["uri"]
    assert (
        encodable["seller_fee_basis_points"] == expected_data["seller_fee_basis_points"]
    )
    assert len(encodable["creators"]) == len(expected_data["creators"])
    assert encodable["primary_sale_happened"] == expected_data["primary_sale_happened"]
    assert encodable["is_mutable"] == expected_data["is_mutable"]
    assert encodable["token_standard"] == expected_data["token_standard"]
    assert encodable["collection"] == expected_data["collection"]
    assert encodable["uses"] == expected_data["uses"]
    assert encodable["collection_details"] == expected_data["collection_details"]
    assert encodable["rule_set"] == expected_data["rule_set"]


def test_asset_data_from_decoded():
    decoded = Container(
        name="Example Name",
        symbol="EXM",
        uri="https://example.com",
        seller_fee_basis_points=500,
        creators=[Container(address=Pubkey.new_unique(), verified=False, share=100)],
        primary_sale_happened=False,
        is_mutable=True,
        token_standard={"NonFungible": {}},
        collection=Container(verified=False, key=Pubkey.new_unique()),
        uses=Container(use_method={"Single": {}}, remaining=5, total=5),
        collection_details={"V1": {"size": 5}},
        rule_set=None,
    )
    args = AssetData.from_decoded(decoded)

    assert args.name == decoded.name
    assert args.symbol == decoded.symbol
    assert args.uri == decoded.uri
    assert args.seller_fee_basis_points == decoded.seller_fee_basis_points
    assert len(args.creators) == len(decoded.creators)
    assert args.primary_sale_happened == decoded.primary_sale_happened
    assert args.is_mutable == decoded.is_mutable
    assert args.token_standard == NonFungible()
    assert args.collection.verified == decoded.collection.verified
    assert args.uses == Uses(use_method=Single(), remaining=5, total=5)
    assert args.collection_details == V1(value={"size": 5})
    assert args.rule_set == decoded.rule_set


def test_asset_data_to_json():
    args = AssetData(
        name="Example Name",
        symbol="EXM",
        uri="https://example.com",
        seller_fee_basis_points=500,
        creators=[
            creator.Creator(address=Pubkey.new_unique(), verified=False, share=100)
        ],
        primary_sale_happened=False,
        is_mutable=True,
        token_standard=token_standard.NonFungible,
        collection=collection.Collection(verified=False, key=Pubkey.new_unique()),
        uses=Uses(use_method=Single(), remaining=5, total=5),
        collection_details=collection_details.V1(value={"size": 5}),
        rule_set=None,
    )
    json_obj = args.to_json()
    assert json_obj["name"] == args.name
    assert json_obj["symbol"] == args.symbol
    assert json_obj["uri"] == args.uri
    assert json_obj["seller_fee_basis_points"] == args.seller_fee_basis_points
    assert len(json_obj["creators"]) == len(args.creators)
    assert json_obj["primary_sale_happened"] == args.primary_sale_happened
    assert json_obj["is_mutable"] == args.is_mutable
    assert json_obj["token_standard"] == args.token_standard.to_json()
    assert json_obj["collection"] == args.collection.to_json()
    assert json_obj["uses"] == args.uses.to_json()
    assert json_obj["collection_details"] == args.collection_details.to_json()
    assert json_obj["rule_set"] == args.rule_set


def test_asset_data_from_json():
    json_obj = {
        "name": "Example Name",
        "symbol": "EXM",
        "uri": "https://example.com",
        "seller_fee_basis_points": 500,
        "creators": [
            {"address": str(Pubkey.new_unique()), "verified": False, "share": 100}
        ],
        "primary_sale_happened": False,
        "is_mutable": True,
        "token_standard": token_standard.NonFungible().to_json(),
        "collection": {"verified": False, "key": str(Pubkey.new_unique())},
        "uses": Uses(use_method=Single(), remaining=5, total=5).to_json(),
        "collection_details": collection_details.V1(value={"size": 5}).to_json(),
        "rule_set": str(Pubkey.new_unique()),
    }
    args = AssetData.from_json(json_obj)
    assert args.name == json_obj["name"]
    assert args.symbol == json_obj["symbol"]
    assert args.uri == json_obj["uri"]
    assert args.seller_fee_basis_points == json_obj["seller_fee_basis_points"]
    assert len(args.creators) == len(json_obj["creators"])
    assert args.primary_sale_happened == json_obj["primary_sale_happened"]
    assert args.is_mutable == json_obj["is_mutable"]
    assert args.token_standard == NonFungible()
    assert args.collection.verified == json_obj["collection"]["verified"]
    assert args.collection.key == Pubkey.from_string(json_obj["collection"]["key"])
    assert args.uses.use_method == Single()
    assert args.uses.remaining == json_obj["uses"]["remaining"]
    assert args.uses.total == json_obj["uses"]["total"]
    assert args.collection_details == collection_details.V1(value={"size": 5})
    assert args.rule_set == Pubkey.from_string(json_obj["rule_set"])
