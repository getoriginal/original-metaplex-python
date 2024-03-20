from original_metaplex_python.token_metadata.generated.types import (
    Payload,
    authorization_data,
    mint_args,
)
from original_metaplex_python.token_metadata.generated.types.mint_args import V1


def test_mint_args_to_encodable_v1():
    auth_data = authorization_data.AuthorizationData(payload=Payload(map=True))
    instance = V1(value={"amount": 100, "authorization_data": auth_data})
    encodable = instance.to_encodable()
    assert encodable == {
        "V1": {
            "amount": 100,
            "authorization_data": auth_data.to_encodable(),
        },
    }


def test_mint_args_from_decoded_v1():
    decoded = {"V1": {"amount": 100, "authorization_data": None}}
    instance = mint_args.from_decoded(decoded)
    assert isinstance(instance, V1)
    assert instance.value["amount"] == 100
    assert instance.value["authorization_data"] is None


def test_mint_args_to_json_v1():
    auth_data = authorization_data.AuthorizationData(payload=Payload(map=True))
    instance = V1(value={"amount": 100, "authorization_data": auth_data})
    json_obj = instance.to_json()
    assert json_obj == {
        "kind": "V1",
        "value": {
            "amount": 100,
            "authorization_data": auth_data.to_json(),
        },
    }


def test_mint_args_from_json_v1():
    json_obj = {
        "kind": "V1",
        "value": {
            "amount": 100,
            "authorization_data": None,
        },
    }
    instance = mint_args.from_json(json_obj)
    assert isinstance(instance, V1)
    assert instance.value["amount"] == 100
    assert instance.value["authorization_data"] is None
