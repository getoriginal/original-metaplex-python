from construct import Container

from src.token_metadata.generated.types import Payload


def test_payload_to_encodable():
    payload = Payload(map=True)
    encodable = payload.to_encodable()
    assert encodable == {"map": True}


def test_payload_from_decoded():
    decoded = Container(map=True)
    payload = Payload.from_decoded(decoded)
    assert payload.map is True


def test_payload_to_json():
    payload = Payload(map=True)
    json_obj = payload.to_json()
    assert json_obj == {"map": True}


def test_payload_from_json():
    json_obj = {"map": True}
    payload = Payload.from_json(json_obj)
    assert payload.map is True
