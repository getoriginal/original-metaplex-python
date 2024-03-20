from construct import Container
from solders.pubkey import Pubkey

from src.token_metadata.generated.types import Creator


def test_creator_to_json():
    creator_instance = Creator(address=Pubkey.new_unique(), verified=True, share=100)
    json_data = creator_instance.to_json()
    assert json_data["verified"] is True
    assert json_data["share"] == 100
    assert isinstance(json_data["address"], str)


def test_creator_from_json():
    json_data = {"address": str(Pubkey.new_unique()), "verified": True, "share": 100}
    creator_instance = Creator.from_json(json_data)
    assert creator_instance.verified is True
    assert creator_instance.share == 100
    assert isinstance(creator_instance.address, Pubkey)


def test_creator_to_encodable():
    creator_instance = Creator(address=Pubkey.new_unique(), verified=True, share=100)
    encodable = creator_instance.to_encodable()
    assert encodable["verified"] is True
    assert encodable["share"] == 100
    assert isinstance(encodable["address"], Pubkey)


def test_creator_from_decoded():
    decoded = Container(address=Pubkey.new_unique(), verified=True, share=100)
    creator_instance = Creator.from_decoded(decoded)
    assert creator_instance.verified is True
    assert creator_instance.share == 100
    assert isinstance(creator_instance.address, Pubkey)
