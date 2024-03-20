from construct import Container

from original_metaplex_python.token_metadata.generated.types import (
    AuthorizationData,
    Payload,
)


def test_authorization_data_from_decoded():
    decoded = Container(payload=Container(map=True))
    auth_data = AuthorizationData.from_decoded(decoded)
    assert auth_data.payload.map == decoded.payload.map


def test_authorization_data_to_encodable():
    auth_data = AuthorizationData(payload=Payload(map=True))
    encodable = auth_data.to_encodable()
    expected = {"payload": {"map": True}}
    assert encodable == expected


def test_authorization_data_to_json():
    auth_data = AuthorizationData(payload=Payload(map=True))
    json_data = auth_data.to_json()
    expected = {"payload": {"map": True}}
    assert json_data == expected


def test_authorization_data_from_json():
    json_data = {"payload": {"map": True}}
    auth_data = AuthorizationData.from_json(json_data)
    assert auth_data.payload.map == json_data["payload"]["map"]
