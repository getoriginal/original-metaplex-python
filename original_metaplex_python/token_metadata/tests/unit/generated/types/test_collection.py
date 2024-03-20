from construct import Container
from solders.pubkey import Pubkey

from original_metaplex_python.token_metadata.generated.types import Collection


def test_collection_from_decoded():
    decoded = Container(verified=True, key=Pubkey.new_unique())
    collection_instance = Collection.from_decoded(decoded)
    assert collection_instance.verified == decoded.verified
    assert collection_instance.key == decoded.key


def test_collection_to_encodable():
    key = Pubkey.new_unique()
    collection_instance = Collection(verified=True, key=key)
    encodable = collection_instance.to_encodable()
    expected = {"verified": True, "key": key}
    assert encodable == expected


def test_collection_to_json():
    key = Pubkey.new_unique()
    collection_instance = Collection(verified=True, key=key)
    json_data = collection_instance.to_json()
    expected = {"verified": True, "key": str(key)}
    assert json_data == expected


def test_collection_from_json():
    key_str = str(Pubkey.new_unique())
    json_data = {"verified": True, "key": key_str}
    collection_instance = Collection.from_json(json_data)
    assert collection_instance.verified == json_data["verified"]
    assert str(collection_instance.key) == key_str
