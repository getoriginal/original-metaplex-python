from original_metaplex_python.token_metadata.generated.types import Payload
from original_metaplex_python.token_metadata.generated.types.authorization_data import (
    AuthorizationData,
)
from original_metaplex_python.token_metadata.generated.types.transfer_args import (
    V1,
    from_decoded,
    from_json,
)


def test_transfer_args_v1_to_encodable():
    authorization_data = AuthorizationData(payload=Payload(map=True))
    v1 = V1(value={"amount": 100, "authorization_data": authorization_data})
    encodable = v1.to_encodable()
    assert encodable == {
        "V1": {
            "amount": 100,
            "authorization_data": authorization_data.to_encodable(),
        }
    }


def test_transfer_args_v1_from_decoded():
    decoded = {
        "V1": {
            "amount": 100,
            "authorization_data": AuthorizationData(Payload(map=True)),
        }
    }
    v1 = from_decoded(decoded)
    assert isinstance(v1, V1) and v1.value["amount"] == 100


def test_transfer_args_v1_to_json():
    authorization_data = AuthorizationData(Payload(map=True))
    v1 = V1(value={"amount": 100, "authorization_data": authorization_data})
    json_obj = v1.to_json()
    assert json_obj == {
        "kind": "V1",
        "value": {
            "amount": 100,
            "authorization_data": authorization_data.to_json(),
        },
    }


def test_transfer_args_v1_from_json():
    json_obj = {
        "kind": "V1",
        "value": {
            "amount": 100,
            "authorization_data": {"payload": {"map": True}},
        },
    }
    v1 = from_json(json_obj)
    assert isinstance(v1, V1) and v1.value["amount"] == 100


def test_transfer_args_v1_dataclass():
    authorization_data = AuthorizationData(Payload(map=True))
    v1 = V1(value={"amount": 100, "authorization_data": authorization_data})
    assert v1.value["amount"] == 100
    assert v1.value["authorization_data"] == authorization_data
