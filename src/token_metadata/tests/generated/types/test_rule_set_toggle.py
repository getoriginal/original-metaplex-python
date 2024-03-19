from dataclasses import asdict

from solders.pubkey import Pubkey

from src.token_metadata.generated.types.rule_set_toggle import (
    Clear,
    None_,
    Set,
    from_json,
)


def test_rule_set_toggle_kinds_to_encodable():
    pubkey = Pubkey.new_unique()
    kinds = [None_(), Clear(), Set(value=(pubkey,))]
    for kind in kinds:
        encodable = kind.to_encodable()
        expected = (
            {"None": {}}
            if isinstance(kind, None_)
            else (
                {"Clear": {}}
                if isinstance(kind, Clear)
                else {"Set": {"item_0": pubkey}}
            )
        )
        assert encodable == expected


def test_rule_set_toggle_kinds_to_json():
    pubkey = Pubkey.new_unique()
    kinds = [None_(), Clear(), Set(value=(pubkey,))]
    for kind in kinds:
        json_obj = kind.to_json()
        expected = (
            {"kind": "None"}
            if isinstance(kind, None_)
            else (
                {"kind": "Clear"}
                if isinstance(kind, Clear)
                else {"kind": "Set", "value": (str(pubkey),)}
            )
        )
        assert json_obj == expected


def test_rule_set_toggle_kinds_from_json():
    pubkey_str = str(Pubkey.new_unique())
    kinds_json = [
        {"kind": "None"},
        {"kind": "Clear"},
        {"kind": "Set", "value": (pubkey_str,)},
    ]
    for kind_json in kinds_json:
        kind = from_json(kind_json)
        assert kind.kind == kind_json["kind"]
        if kind.kind == "Set":
            assert str(kind.value[0]) == pubkey_str


def test_rule_set_toggle_kinds_dataclass():
    pubkey = Pubkey.new_unique()
    kinds = [None_(), Clear(), Set(value=pubkey)]
    for kind in kinds:
        dataclass_dict = asdict(kind)
        expected = {"value": pubkey} if isinstance(kind, Set) else {}
        assert dataclass_dict == expected
