from dataclasses import asdict

from original_metaplex_python.token_metadata.generated.types.print_args import (
    V1,
    from_decoded,
    from_json,
)


def test_print_args_to_encodable():
    v1 = V1(value={"edition": 5})
    encodable = v1.to_encodable()
    assert encodable == {"V1": {"edition": 5}}


def test_print_args_v1_from_decoded():
    decoded = {"V1": {"edition": 5}}
    v1 = from_decoded(decoded)
    assert v1.value["edition"] == 5


def test_print_args_v1_to_json():
    v1 = V1(value={"edition": 5})
    json_obj = v1.to_json()
    assert json_obj == {"kind": "V1", "value": {"edition": 5}}


def test_print_args_v1_from_json():
    json_obj = {"kind": "V1", "value": {"edition": 5}}
    v1 = from_json(json_obj)
    assert v1.value["edition"] == 5


def test_print_args_v1_dataclass():
    v1 = V1(value={"edition": 5})
    assert asdict(v1) == {"value": {"edition": 5}}
