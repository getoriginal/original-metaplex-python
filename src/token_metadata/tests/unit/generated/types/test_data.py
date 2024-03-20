from construct import Container
from solders.pubkey import Pubkey

from src.token_metadata.generated.types import Data, creator


def test_data_to_json():
    creator_instance = creator.Creator(
        address=Pubkey.new_unique(), verified=True, share=100
    )
    data_instance = Data(
        name="Test Name",
        symbol="TST",
        uri="https://example.com",
        seller_fee_basis_points=500,
        creators=[creator_instance],
    )
    json_data = data_instance.to_json()
    assert json_data["name"] == "Test Name"
    assert json_data["symbol"] == "TST"
    assert json_data["uri"] == "https://example.com"
    assert json_data["seller_fee_basis_points"] == 500
    assert len(json_data["creators"]) == 1
    assert json_data["creators"][0]["verified"]


def test_data_from_json():
    json_data = {
        "name": "Test Name",
        "symbol": "TST",
        "uri": "https://example.com",
        "seller_fee_basis_points": 500,
        "creators": [
            {"address": str(Pubkey.new_unique()), "verified": True, "share": 100}
        ],
    }
    data_instance = Data.from_json(json_data)
    assert data_instance.name == "Test Name"
    assert data_instance.symbol == "TST"
    assert data_instance.uri == "https://example.com"
    assert data_instance.seller_fee_basis_points == 500
    assert len(data_instance.creators) == 1
    assert data_instance.creators[0].verified


def test_data_to_encodable():
    creator_instance = creator.Creator(
        address=Pubkey.new_unique(), verified=True, share=100
    )
    data_instance = Data(
        name="Test Name",
        symbol="TST",
        uri="https://example.com",
        seller_fee_basis_points=500,
        creators=[creator_instance],
    )
    encodable = data_instance.to_encodable()
    assert encodable["name"] == "Test Name"
    assert encodable["symbol"] == "TST"
    assert encodable["uri"] == "https://example.com"
    assert encodable["seller_fee_basis_points"] == 500
    assert len(encodable["creators"]) == 1
    assert encodable["creators"][0]["verified"]


def test_data_from_decoded():
    creators = [creator.Creator(address=Pubkey.new_unique(), verified=True, share=100)]
    decoded = Container(
        name="Test Name",
        symbol="TST",
        uri="https://example.com",
        seller_fee_basis_points=500,
        creators=creators,
    )
    data_instance = Data.from_decoded(decoded)
    assert data_instance.name == "Test Name"
    assert data_instance.symbol == "TST"
    assert data_instance.uri == "https://example.com"
    assert data_instance.seller_fee_basis_points == 500
    assert len(data_instance.creators) == 1
    assert data_instance.creators[0].verified
