from dataclasses import asdict

from original_metaplex_python.token_metadata.generated.types.token_state import (
    Listed,
    Locked,
    Unlocked,
    from_decoded,
    from_json,
)


def test_token_state_to_encodable():
    kinds = [Unlocked(), Locked(), Listed()]
    for kind in kinds:
        encodable = kind.to_encodable()
        assert encodable == {kind.kind: {}}


def test_token_state_from_decoded():
    kinds_dict = [{"Unlocked": {}}, {"Locked": {}}, {"Listed": {}}]
    for kind_dict in kinds_dict:
        kind = from_decoded(kind_dict)
        assert kind.kind in kind_dict


def test_token_state_to_json():
    kinds = [Unlocked(), Locked(), Listed()]
    for kind in kinds:
        json_obj = kind.to_json()
        assert json_obj == {"kind": kind.kind}


def test_token_state_from_json():
    kinds_json = [{"kind": "Unlocked"}, {"kind": "Locked"}, {"kind": "Listed"}]
    for kind_json in kinds_json:
        kind = from_json(kind_json)
        assert kind.kind == kind_json["kind"]


def test_token_state_dataclass():
    kinds = [Unlocked(), Locked(), Listed()]
    for kind in kinds:
        assert asdict(kind) == {}
