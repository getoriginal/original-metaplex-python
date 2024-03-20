from original_metaplex_python.token_metadata.generated.types import Payload
from original_metaplex_python.token_metadata.generated.types.authorization_data import (
    AuthorizationData,
)
from original_metaplex_python.token_metadata.generated.types.unlock_args import (
    V1,
    from_decoded,
    from_json,
)


def test_unlock_args_v1_to_encodable():
    auth_data = AuthorizationData(payload=Payload(map=True))
    v1 = V1(value={"authorization_data": auth_data})
    encodable = v1.to_encodable()
    assert encodable == {"V1": {"authorization_data": auth_data.to_encodable()}}


def test_unlock_args_v1_from_decoded():
    decoded = {
        "V1": {"authorization_data": AuthorizationData(payload=Payload(map=True))}
    }
    v1 = from_decoded(decoded)
    assert isinstance(v1, V1) and v1.value["authorization_data"].payload.map is True


def test_unlock_args_v1_to_json():
    auth_data = AuthorizationData(payload=Payload(map=True))
    v1 = V1(value={"authorization_data": auth_data})
    json_obj = v1.to_json()
    assert json_obj == {
        "kind": "V1",
        "value": {"authorization_data": auth_data.to_json()},
    }


def test_unlock_args_v1_from_json():
    json_obj = {
        "kind": "V1",
        "value": {"authorization_data": {"payload": {"map": True}}},
    }
    v1 = from_json(json_obj)
    assert isinstance(v1, V1) and v1.value["authorization_data"].payload.map is True


def test_unlock_args_v1_dataclass():
    auth_data = AuthorizationData(payload=Payload(map=True))
    v1 = V1(value={"authorization_data": auth_data})
    assert v1.value["authorization_data"].payload.map is True
