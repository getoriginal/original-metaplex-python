from src.token_metadata.generated.types.use_method import (
    Burn,
    Multiple,
    Single,
    from_decoded,
    from_json,
)


def test_use_method_burn_to_encodable():
    burn = Burn()
    encodable = burn.to_encodable()
    assert encodable == {"Burn": {}}


def test_use_method_burn_from_decoded():
    decoded = {"Burn": {}}
    burn = from_decoded(decoded)
    assert isinstance(burn, Burn)


def test_use_method_burn_to_json():
    burn = Burn()
    json_obj = burn.to_json()
    assert json_obj == {"kind": "Burn"}


def test_use_method_burn_from_json():
    json_obj = {"kind": "Burn"}
    burn = from_json(json_obj)
    assert isinstance(burn, Burn)


def test_use_method_multiple_to_encodable():
    multiple = Multiple()
    encodable = multiple.to_encodable()
    assert encodable == {"Multiple": {}}


def test_use_method_multiple_from_decoded():
    decoded = {"Multiple": {}}
    multiple = from_decoded(decoded)
    assert isinstance(multiple, Multiple)


def test_use_method_multiple_to_json():
    multiple = Multiple()
    json_obj = multiple.to_json()
    assert json_obj == {"kind": "Multiple"}


def test_use_method_multiple_from_json():
    json_obj = {"kind": "Multiple"}
    multiple = from_json(json_obj)
    assert isinstance(multiple, Multiple)


def test_use_method_single_to_encodable():
    single = Single()
    encodable = single.to_encodable()
    assert encodable == {"Single": {}}


def test_use_method_single_from_decoded():
    decoded = {"Single": {}}
    single = from_decoded(decoded)
    assert isinstance(single, Single)


def test_use_method_single_to_json():
    single = Single()
    json_obj = single.to_json()
    assert json_obj == {"kind": "Single"}


def test_use_method_single_from_json():
    json_obj = {"kind": "Single"}
    single = from_json(json_obj)
    assert isinstance(single, Single)
