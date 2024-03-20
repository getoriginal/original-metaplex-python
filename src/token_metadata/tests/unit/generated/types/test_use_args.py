from src.token_metadata.generated.types import Payload
from src.token_metadata.generated.types.authorization_data import AuthorizationData
from src.token_metadata.generated.types.use_args import V1, from_decoded, from_json

authorization_data_example = AuthorizationData(Payload(map=True))


def test_use_args_v1_to_encodable():
    v1 = V1(value={"authorization_data": authorization_data_example})
    encodable = v1.to_encodable()
    assert encodable == {
        "V1": {"authorization_data": authorization_data_example.to_encodable()}
    }


def test_use_args_v1_from_decoded():
    decoded = {"V1": {"authorization_data": authorization_data_example}}
    v1 = from_decoded(decoded)
    assert isinstance(v1, V1) and v1.value["authorization_data"].payload == Payload(
        map=True
    )


def test_use_args_v1_to_json():
    v1 = V1(value={"authorization_data": authorization_data_example})
    json_obj = v1.to_json()
    assert json_obj == {
        "kind": "V1",
        "value": {"authorization_data": authorization_data_example.to_json()},
    }


def test_use_args_v1_from_json():
    authorization_data_json = {"payload": {"map": True}}
    json_obj = {"kind": "V1", "value": {"authorization_data": authorization_data_json}}
    v1 = from_json(json_obj)
    assert isinstance(v1, V1) and v1.value["authorization_data"].payload == Payload(
        map=True
    )
