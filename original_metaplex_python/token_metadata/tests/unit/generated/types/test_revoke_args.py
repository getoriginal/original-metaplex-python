from dataclasses import asdict

from original_metaplex_python.token_metadata.generated.types.revoke_args import (
    AuthorityItemV1,
    CollectionItemV1,
    CollectionV1,
    DataItemV1,
    DataV1,
    LockedTransferV1,
    MigrationV1,
    ProgrammableConfigItemV1,
    ProgrammableConfigV1,
    SaleV1,
    StakingV1,
    StandardV1,
    TransferV1,
    UtilityV1,
    from_json,
)


def test_revoke_args_kinds_to_encodable():
    kinds = [
        CollectionV1(),
        SaleV1(),
        TransferV1(),
        DataV1(),
        UtilityV1(),
        StakingV1(),
        StandardV1(),
        LockedTransferV1(),
        ProgrammableConfigV1(),
        MigrationV1(),
        AuthorityItemV1(),
        DataItemV1(),
        CollectionItemV1(),
        ProgrammableConfigItemV1(),
    ]
    for kind in kinds:
        encodable = kind.to_encodable()
        assert encodable == {kind.kind: {}}


def test_revoke_args_kinds_to_json():
    kinds = [
        CollectionV1(),
        SaleV1(),
        TransferV1(),
        DataV1(),
        UtilityV1(),
        StakingV1(),
        StandardV1(),
        LockedTransferV1(),
        ProgrammableConfigV1(),
        MigrationV1(),
        AuthorityItemV1(),
        DataItemV1(),
        CollectionItemV1(),
        ProgrammableConfigItemV1(),
    ]
    for kind in kinds:
        json_obj = kind.to_json()
        assert json_obj == {"kind": kind.kind}


def test_revoke_args_kinds_from_json():
    kinds_json = [
        {"kind": "CollectionV1"},
        {"kind": "SaleV1"},
        {"kind": "TransferV1"},
        {"kind": "DataV1"},
        {"kind": "UtilityV1"},
        {"kind": "StakingV1"},
        {"kind": "StandardV1"},
        {"kind": "LockedTransferV1"},
        {"kind": "ProgrammableConfigV1"},
        {"kind": "MigrationV1"},
        {"kind": "AuthorityItemV1"},
        {"kind": "DataItemV1"},
        {"kind": "CollectionItemV1"},
        {"kind": "ProgrammableConfigItemV1"},
    ]
    for kind_json in kinds_json:
        kind = from_json(kind_json)
        assert kind.kind == kind_json["kind"]


def test_revoke_args_kinds_dataclass():
    kinds = [
        CollectionV1(),
        SaleV1(),
        TransferV1(),
        DataV1(),
        UtilityV1(),
        StakingV1(),
        StandardV1(),
        LockedTransferV1(),
        ProgrammableConfigV1(),
        MigrationV1(),
        AuthorityItemV1(),
        DataItemV1(),
        CollectionItemV1(),
        ProgrammableConfigItemV1(),
    ]
    for kind in kinds:
        assert asdict(kind) == {}
