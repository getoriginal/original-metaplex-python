from construct import Container

from original_metaplex_python.token_metadata.generated.types import Payload, lock_args
from original_metaplex_python.token_metadata.generated.types.authorization_data import (
    AuthorizationData,
)
from original_metaplex_python.token_metadata.generated.types.lock_args import V1


def test_lock_args_v1_to_encodable():
    authorization_data_instance = AuthorizationData(payload=Payload(map=True))
    v1_instance = V1(value={"authorization_data": authorization_data_instance})
    encodable = v1_instance.to_encodable()

    assert encodable == {
        "V1": {
            "authorization_data": authorization_data_instance.to_encodable(),
        },
    }


def test_lock_args_v1_from_decoded():
    decoded = Container(
        V1=Container(authorization_data=Container(payload=Payload(map=True)))
    )
    v1_instance = lock_args.from_decoded(decoded)

    assert isinstance(v1_instance, V1)
    assert v1_instance.value["authorization_data"].payload == Payload(map=True)


def test_lock_args_v1_to_json():
    authorization_data_instance = AuthorizationData(payload=Payload(map=True))
    v1_instance = V1(value={"authorization_data": authorization_data_instance})
    json_obj = v1_instance.to_json()

    assert json_obj == {
        "kind": "V1",
        "value": {
            "authorization_data": authorization_data_instance.to_json(),
        },
    }


def test_lock_args_v1_from_json():
    json_obj = {
        "kind": "V1",
        "value": {"authorization_data": {"payload": {"map": True}}},
    }
    v1_instance = lock_args.from_json(json_obj)

    assert isinstance(v1_instance, V1)
    assert v1_instance.value["authorization_data"].payload == Payload(map=True)
