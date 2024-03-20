from construct import Container
from solders.pubkey import Pubkey

from original_metaplex_python.token_metadata.generated.types import Collection
from original_metaplex_python.token_metadata.generated.types.collection_toggle import (
    Clear,
    None_,
    Set,
    from_decoded,
    from_json,
)


def test_none_to_json():
    none_instance = None_.to_json()
    expected = {"kind": "None"}
    assert none_instance == expected


def test_none_to_encodable():
    none_encodable = None_.to_encodable()
    expected = {"None": {}}
    assert none_encodable == expected


def test_clear_to_json():
    clear_instance = Clear.to_json()
    expected = {"kind": "Clear"}
    assert clear_instance == expected


def test_clear_to_encodable():
    clear_encodable = Clear.to_encodable()
    expected = {"Clear": {}}
    assert clear_encodable == expected


def test_set_to_json():
    set_instance = Set(value=(Collection(verified=True, key=Pubkey.new_unique()),))
    json_data = set_instance.to_json()
    expected = {
        "kind": "Set",
        "value": [{"verified": True, "key": str(set_instance.value[0].key)}],
    }
    assert json_data["kind"] == expected["kind"]
    assert json_data["value"][0]["verified"] == expected["value"][0]["verified"]
    assert json_data["value"][0]["key"] == expected["value"][0]["key"]


def test_set_to_encodable():
    set_instance = Set(value=(Collection(verified=True, key=Pubkey.new_unique()),))
    encodable = set_instance.to_encodable()
    expected = {
        "Set": {
            "item_0": {"verified": True, "key": set_instance.value[0].key},
        },
    }
    assert encodable == expected


def test_from_decoded_none():
    decoded = {"None": {}}
    instance = from_decoded(decoded)
    assert isinstance(instance, None_)


def test_from_decoded_clear():
    decoded = {"Clear": {}}
    instance = from_decoded(decoded)
    assert isinstance(instance, Clear)


def test_from_decoded_set():
    decoded = {"Set": {"item_0": Container(verified=True, key=Pubkey.new_unique())}}
    instance = from_decoded(decoded)
    assert isinstance(instance, Set)
    assert isinstance(instance.value[0].key, Pubkey)


def test_from_json_none():
    json_data = {"kind": "None"}
    instance = from_json(json_data)
    assert isinstance(instance, None_)


def test_from_json_clear():
    json_data = {"kind": "Clear"}
    instance = from_json(json_data)
    assert isinstance(instance, Clear)


def test_from_json_set():
    key = str(Pubkey.new_unique())
    json_data = {
        "kind": "Set",
        "value": [{"verified": True, "key": key}],
    }
    instance = from_json(json_data)
    assert isinstance(instance, Set)
    assert instance.value[0].verified is True
    assert str(instance.value[0].key) == key
