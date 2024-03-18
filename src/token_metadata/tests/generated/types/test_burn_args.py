from src.token_metadata.generated.types.burn_args import V1, from_decoded, from_json


def test_v1_to_json():
    v1_instance = V1(value={"amount": 100})
    json_data = v1_instance.to_json()
    expected = {"kind": "V1", "value": {"amount": 100}}
    assert json_data == expected


def test_v1_to_encodable():
    v1_instance = V1(value={"amount": 100})
    encodable = v1_instance.to_encodable()
    expected = {"V1": {"amount": 100}}
    assert encodable == expected


def test_from_decoded_v1():
    decoded = {"V1": {"amount": 100}}
    v1_instance = from_decoded(decoded)
    assert isinstance(v1_instance, V1)
    assert v1_instance.value == {"amount": 100}


def test_from_json_v1():
    json_data = {"kind": "V1", "value": {"amount": 100}}
    v1_instance = from_json(json_data)
    assert isinstance(v1_instance, V1)
    assert v1_instance.value == {"amount": 100}


def test_from_decoded_invalid():
    decoded = {"InvalidKind": {"amount": 100}}
    try:
        from_decoded(decoded)
    except ValueError as e:
        assert str(e) == "Invalid enum object"


def test_from_json_invalid_kind():
    json_data = {"kind": "InvalidKind", "value": {"amount": 100}}
    try:
        from_json(json_data)
    except ValueError as e:
        assert str(e).startswith("Unrecognized enum kind:")
