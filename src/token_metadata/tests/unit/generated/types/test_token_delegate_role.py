from dataclasses import asdict

from src.token_metadata.generated.types.token_delegate_role import (
    LockedTransfer,
    Migration,
    Sale,
    Staking,
    Standard,
    Transfer,
    Utility,
    from_decoded,
    from_json,
)


def test_token_delegate_role_to_encodable():
    roles = [
        Sale(),
        Transfer(),
        Utility(),
        Staking(),
        Standard(),
        LockedTransfer(),
        Migration(),
    ]
    for role in roles:
        encodable = role.to_encodable()
        assert encodable == {role.kind: {}}


def test_token_delegate_role_from_decoded():
    roles_dict = [
        {"Sale": {}},
        {"Transfer": {}},
        {"Utility": {}},
        {"Staking": {}},
        {"Standard": {}},
        {"LockedTransfer": {}},
        {"Migration": {}},
    ]
    for role_dict in roles_dict:
        role = from_decoded(role_dict)
        assert role.kind in role_dict


def test_token_delegate_role_to_json():
    roles = [
        Sale(),
        Transfer(),
        Utility(),
        Staking(),
        Standard(),
        LockedTransfer(),
        Migration(),
    ]
    for role in roles:
        json_obj = role.to_json()
        assert json_obj == {"kind": role.kind}


def test_token_delegate_role_from_json():
    roles_json = [
        {"kind": "Sale"},
        {"kind": "Transfer"},
        {"kind": "Utility"},
        {"kind": "Staking"},
        {"kind": "Standard"},
        {"kind": "LockedTransfer"},
        {"kind": "Migration"},
    ]
    for role_json in roles_json:
        role = from_json(role_json)
        assert role.kind == role_json["kind"]


def test_token_delegate_role_dataclass():
    roles = [
        Sale(),
        Transfer(),
        Utility(),
        Staking(),
        Standard(),
        LockedTransfer(),
        Migration(),
    ]
    for role in roles:
        assert asdict(role) == {}
