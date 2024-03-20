from construct import Container
from solders.pubkey import Pubkey

from src.token_metadata.generated.types import DataV2, Uses, collection, creator, uses
from src.token_metadata.generated.types.use_method import Single


def test_data_v2_to_json():
    creator_instance = creator.Creator(
        address=Pubkey.new_unique(), verified=True, share=100
    )
    collection_instance = collection.Collection(verified=True, key=Pubkey.new_unique())
    uses_instance = uses.Uses(use_method=Single, remaining=5, total=5)
    data_v2_instance = DataV2(
        name="Asset Name",
        symbol="ASN",
        uri="https://example.com",
        seller_fee_basis_points=100,
        creators=[creator_instance],
        collection=collection_instance,
        uses=uses_instance,
    )
    json_data = data_v2_instance.to_json()
    assert json_data["name"] == "Asset Name"
    assert json_data["symbol"] == "ASN"
    assert json_data["uri"] == "https://example.com"
    assert json_data["seller_fee_basis_points"] == 100
    assert len(json_data["creators"]) == 1
    assert json_data["creators"][0]["verified"]
    assert json_data["collection"]["verified"]
    assert json_data["uses"]["use_method"] == {"kind": "Single"}


def test_data_v2_from_json():
    json_data = {
        "name": "Asset Name",
        "symbol": "ASN",
        "uri": "https://example.com",
        "seller_fee_basis_points": 100,
        "creators": [
            {"address": str(Pubkey.new_unique()), "verified": True, "share": 100}
        ],
        "collection": {"verified": True, "key": str(Pubkey.new_unique())},
        "uses": Uses(use_method=Single(), remaining=5, total=5).to_json(),
    }
    data_v2_instance = DataV2.from_json(json_data)
    assert data_v2_instance.name == "Asset Name"
    assert data_v2_instance.symbol == "ASN"
    assert data_v2_instance.uri == "https://example.com"
    assert data_v2_instance.seller_fee_basis_points == 100
    assert len(data_v2_instance.creators) == 1
    assert data_v2_instance.creators[0].verified
    assert data_v2_instance.collection.verified
    assert data_v2_instance.uses.use_method == Single()


def test_data_v2_to_encodable():
    creator_instance = creator.Creator(
        address=Pubkey.new_unique(), verified=True, share=100
    )
    collection_instance = collection.Collection(verified=True, key=Pubkey.new_unique())
    uses_instance = uses.Uses(use_method=Single, remaining=5, total=5)
    data_v2_instance = DataV2(
        name="Asset Name",
        symbol="ASN",
        uri="https://example.com",
        seller_fee_basis_points=100,
        creators=[creator_instance],
        collection=collection_instance,
        uses=uses_instance,
    )
    encodable = data_v2_instance.to_encodable()
    assert encodable["name"] == "Asset Name"
    assert encodable["symbol"] == "ASN"
    assert encodable["uri"] == "https://example.com"
    assert encodable["seller_fee_basis_points"] == 100
    assert len(encodable["creators"]) == 1
    assert encodable["creators"][0]["verified"]
    assert encodable["collection"]["verified"]
    assert encodable["uses"]["use_method"] == {"Single": {}}


def test_data_v2_from_decoded():
    creators_container = [
        Container(address=Pubkey.new_unique(), verified=True, share=100)
    ]
    collection_container = Container(verified=True, key=Pubkey.new_unique())
    uses_container = Container(use_method=Single.to_encodable(), remaining=5, total=5)
    decoded = Container(
        name="Asset Name",
        symbol="ASN",
        uri="https://example.com",
        seller_fee_basis_points=100,
        creators=creators_container,
        collection=collection_container,
        uses=uses_container,
    )
    data_v2_instance = DataV2.from_decoded(decoded)
    assert data_v2_instance.name == "Asset Name"
    assert data_v2_instance.symbol == "ASN"
    assert data_v2_instance.uri == "https://example.com"
    assert data_v2_instance.seller_fee_basis_points == 100
    assert len(data_v2_instance.creators) == 1
    assert data_v2_instance.creators[0].verified
    assert data_v2_instance.collection.verified
    assert data_v2_instance.uses.use_method == Single()
