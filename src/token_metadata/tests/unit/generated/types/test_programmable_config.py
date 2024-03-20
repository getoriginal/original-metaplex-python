from dataclasses import asdict

from solders.pubkey import Pubkey

from src.token_metadata.generated.types.programmable_config import (
    V1,
    from_decoded,
    from_json,
)


def test_programmable_config_v1_to_encodable():
    pubkey = Pubkey.new_unique()
    v1 = V1(value={"rule_set": pubkey})
    encodable = v1.to_encodable()
    assert encodable == {"V1": {"rule_set": pubkey}}


def test_programmable_config_v1_from_decoded():
    pubkey = Pubkey.new_unique()
    decoded = {"V1": {"rule_set": pubkey}}
    v1 = from_decoded(decoded)
    assert isinstance(v1, V1) and v1.value["rule_set"] == pubkey


def test_programmable_config_v1_to_json():
    pubkey = Pubkey.new_unique()
    v1 = V1(value={"rule_set": pubkey})
    json_obj = v1.to_json()
    assert json_obj == {"kind": "V1", "value": {"rule_set": str(pubkey)}}


def test_programmable_config_v1_from_json():
    pubkey_str = str(Pubkey.new_unique())
    json_obj = {"kind": "V1", "value": {"rule_set": pubkey_str}}
    v1 = from_json(json_obj)
    assert isinstance(v1, V1) and str(v1.value["rule_set"]) == pubkey_str


def test_programmable_config_v1_dataclass():
    pubkey = Pubkey.new_unique()
    v1 = V1(value={"rule_set": pubkey})
    assert asdict(v1) == {"value": {"rule_set": pubkey}}
