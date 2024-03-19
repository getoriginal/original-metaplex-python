from src.token_metadata.generated.types.use_method import Burn
from src.token_metadata.generated.types.uses import Uses


def test_uses_to_encodable():
    uses = Uses(use_method=Burn(), remaining=5, total=10)
    encodable = uses.to_encodable()
    assert encodable == {"use_method": {"Burn": {}}, "remaining": 5, "total": 10}


def test_uses_from_decoded():
    decoded = Uses(use_method=Burn.to_encodable(), remaining=5, total=10)
    uses = Uses.from_decoded(decoded)
    assert (
        isinstance(uses, Uses)
        and isinstance(uses.use_method, Burn)
        and uses.remaining == 5
        and uses.total == 10
    )


def test_uses_to_json():
    uses = Uses(use_method=Burn(), remaining=5, total=10)
    json_obj = uses.to_json()
    assert json_obj == {"use_method": {"kind": "Burn"}, "remaining": 5, "total": 10}


def test_uses_from_json():
    json_obj = {"use_method": {"kind": "Burn"}, "remaining": 5, "total": 10}
    uses = Uses.from_json(json_obj)
    assert (
        isinstance(uses, Uses)
        and isinstance(uses.use_method, Burn)
        and uses.remaining == 5
        and uses.total == 10
    )
