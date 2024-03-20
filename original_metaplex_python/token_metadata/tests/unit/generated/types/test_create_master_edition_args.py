from original_metaplex_python.token_metadata.generated.types import (
    CreateMasterEditionArgs,
)


def test_create_master_edition_args_from_decoded():
    decoded = CreateMasterEditionArgs(max_supply=5000)
    args = CreateMasterEditionArgs.from_decoded(decoded)
    assert args.max_supply == 5000


def test_create_master_edition_args_to_encodable():
    args = CreateMasterEditionArgs(max_supply=5000)
    encodable = args.to_encodable()
    expected = {"max_supply": 5000}
    assert encodable == expected


def test_create_master_edition_args_to_json():
    args = CreateMasterEditionArgs(max_supply=5000)
    json_data = args.to_json()
    expected = {"max_supply": 5000}
    assert json_data == expected


def test_create_master_edition_args_from_json():
    json_data = {"max_supply": 5000}
    args = CreateMasterEditionArgs.from_json(json_data)
    assert args.max_supply == 5000


def test_create_master_edition_args_from_decoded_none():
    decoded = CreateMasterEditionArgs(max_supply=None)
    args = CreateMasterEditionArgs.from_decoded(decoded)
    assert args.max_supply is None


def test_create_master_edition_args_to_json_none():
    args = CreateMasterEditionArgs(max_supply=None)
    json_data = args.to_json()
    expected = {"max_supply": None}
    assert json_data == expected


def test_create_master_edition_args_from_json_none():
    json_data = {"max_supply": None}
    args = CreateMasterEditionArgs.from_json(json_data)
    assert args.max_supply is None
