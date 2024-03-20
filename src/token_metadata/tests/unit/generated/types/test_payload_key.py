from src.token_metadata.generated.types.payload_key import (
    Amount,
    Authority,
    AuthoritySeeds,
    Delegate,
    DelegateSeeds,
    Destination,
    DestinationSeeds,
    Holder,
    Source,
    SourceSeeds,
)
from src.token_metadata.generated.types.payload_key import (
    from_decoded as payload_key_from_decoded,
)
from src.token_metadata.generated.types.payload_key import (
    from_json as payload_key_from_json,
)


def test_payload_key_kind_to_json():
    kinds = [
        Amount(),
        Authority(),
        AuthoritySeeds(),
        Delegate(),
        DelegateSeeds(),
        Destination(),
        DestinationSeeds(),
        Holder(),
        Source(),
        SourceSeeds(),
    ]
    for kind in kinds:
        json_obj = kind.to_json()
        assert json_obj["kind"] == kind.kind


def test_payload_key_kind_to_encodable():
    kinds = [
        Amount(),
        Authority(),
        AuthoritySeeds(),
        Delegate(),
        DelegateSeeds(),
        Destination(),
        DestinationSeeds(),
        Holder(),
        Source(),
        SourceSeeds(),
    ]
    for kind in kinds:
        encodable = kind.to_encodable()
        assert list(encodable.keys())[0] == kind.kind


def test_payload_key_kind_from_json():
    kinds_json = [
        {"kind": "Amount"},
        {"kind": "Authority"},
        {"kind": "AuthoritySeeds"},
        {"kind": "Delegate"},
        {"kind": "DelegateSeeds"},
        {"kind": "Destination"},
        {"kind": "DestinationSeeds"},
        {"kind": "Holder"},
        {"kind": "Source"},
        {"kind": "SourceSeeds"},
    ]
    for kind_json in kinds_json:
        kind = payload_key_from_json(kind_json)
        assert kind.kind == kind_json["kind"]


def test_payload_key_kind_from_decoded():
    kinds_decoded = [
        {"Amount": {}},
        {"Authority": {}},
        {"AuthoritySeeds": {}},
        {"Delegate": {}},
        {"DelegateSeeds": {}},
        {"Destination": {}},
        {"DestinationSeeds": {}},
        {"Holder": {}},
        {"Source": {}},
        {"SourceSeeds": {}},
    ]
    for kind_decoded in kinds_decoded:
        kind = payload_key_from_decoded(kind_decoded)
        assert kind.kind == list(kind_decoded.keys())[0]
