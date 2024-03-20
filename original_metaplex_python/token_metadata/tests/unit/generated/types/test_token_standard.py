from dataclasses import asdict

from original_metaplex_python.token_metadata.generated.types.token_standard import (
    Fungible,
    FungibleAsset,
    NonFungible,
    NonFungibleEdition,
    ProgrammableNonFungible,
    ProgrammableNonFungibleEdition,
    from_decoded,
    from_json,
)


def test_token_standard_to_encodable():
    kinds = [
        NonFungible(),
        FungibleAsset(),
        Fungible(),
        NonFungibleEdition(),
        ProgrammableNonFungible(),
        ProgrammableNonFungibleEdition(),
    ]
    for kind in kinds:
        encodable = kind.to_encodable()
        assert encodable == {kind.kind: {}}


def test_token_standard_from_decoded():
    kinds_dict = [
        {"NonFungible": {}},
        {"FungibleAsset": {}},
        {"Fungible": {}},
        {"NonFungibleEdition": {}},
        {"ProgrammableNonFungible": {}},
        {"ProgrammableNonFungibleEdition": {}},
    ]
    for kind_dict in kinds_dict:
        kind = from_decoded(kind_dict)
        assert kind.kind in kind_dict


def test_token_standard_to_json():
    kinds = [
        NonFungible(),
        FungibleAsset(),
        Fungible(),
        NonFungibleEdition(),
        ProgrammableNonFungible(),
        ProgrammableNonFungibleEdition(),
    ]
    for kind in kinds:
        json_obj = kind.to_json()
        assert json_obj == {"kind": kind.kind}


def test_token_standard_from_json():
    kinds_json = [
        {"kind": "NonFungible"},
        {"kind": "FungibleAsset"},
        {"kind": "Fungible"},
        {"kind": "NonFungibleEdition"},
        {"kind": "ProgrammableNonFungible"},
        {"kind": "ProgrammableNonFungibleEdition"},
    ]
    for kind_json in kinds_json:
        kind = from_json(kind_json)
        assert kind.kind == kind_json["kind"]


def test_token_standard_dataclass():
    kinds = [
        NonFungible(),
        FungibleAsset(),
        Fungible(),
        NonFungibleEdition(),
        ProgrammableNonFungible(),
        ProgrammableNonFungibleEdition(),
    ]
    for kind in kinds:
        assert asdict(kind) == {}
