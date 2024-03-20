from original_metaplex_python.token_metadata.generated.types.use_method import Burn
from original_metaplex_python.token_metadata.generated.types.uses import Uses
from original_metaplex_python.token_metadata.generated.types.uses_toggle import (
    Clear,
    None_,
    Set,
    from_decoded,
    from_json,
)


def test_uses_toggle_none_to_encodable():
    none_ = None_()
    encodable = none_.to_encodable()
    assert encodable == {"None": {}}


def test_uses_toggle_clear_to_encodable():
    clear = Clear()
    encodable = clear.to_encodable()
    assert encodable == {"Clear": {}}


def test_uses_toggle_set_to_encodable():
    uses = Uses(use_method=Burn(), remaining=5, total=10)
    set_ = Set(value=(uses,))
    encodable = set_.to_encodable()
    assert encodable == {
        "Set": {"item_0": {"use_method": {"Burn": {}}, "remaining": 5, "total": 10}}
    }


def test_uses_toggle_none_from_decoded():
    decoded = {"None": {}}
    result = from_decoded(decoded)
    assert isinstance(result, None_)


def test_uses_toggle_clear_from_decoded():
    decoded = {"Clear": {}}
    result = from_decoded(decoded)
    assert isinstance(result, Clear)


def test_uses_toggle_set_from_decoded():
    decoded = {
        "Set": {"item_0": Uses(use_method=Burn().to_encodable(), remaining=5, total=10)}
    }
    result = from_decoded(decoded)
    assert result.value[0].use_method == Burn()
    assert result.value[0].remaining == 5
    assert result.value[0].total == 10


def test_uses_toggle_none_from_json():
    json_obj = {"kind": "None"}
    result = from_json(json_obj)
    assert isinstance(result, None_)


def test_uses_toggle_clear_from_json():
    json_obj = {"kind": "Clear"}
    result = from_json(json_obj)
    assert isinstance(result, Clear)


def test_uses_toggle_set_from_json():
    json_obj = {
        "kind": "Set",
        "value": [{"use_method": {"kind": "Burn"}, "remaining": 5, "total": 10}],
    }
    result = from_json(json_obj)
    assert (
        isinstance(result, Set)
        and isinstance(result.value[0], Uses)
        and isinstance(result.value[0].use_method, Burn)
    )
