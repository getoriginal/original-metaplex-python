from construct import Container

from src.token_metadata.generated.types import (
    MintNewEditionFromMasterEditionViaTokenArgs,
)


def test_mint_new_edition_from_master_edition_via_token_args_to_encodable():
    args = MintNewEditionFromMasterEditionViaTokenArgs(edition=42)
    encodable = args.to_encodable()
    assert encodable == {"edition": 42}


def test_mint_new_edition_from_master_edition_via_token_args_from_decoded():
    decoded = Container(edition=42)
    args = MintNewEditionFromMasterEditionViaTokenArgs.from_decoded(decoded)
    assert args.edition == 42


def test_mint_new_edition_from_master_edition_via_token_args_to_json():
    args = MintNewEditionFromMasterEditionViaTokenArgs(edition=42)
    json_obj = args.to_json()
    assert json_obj == {"edition": 42}


def test_mint_new_edition_from_master_edition_via_token_args_from_json():
    json_obj = {"edition": 42}
    args = MintNewEditionFromMasterEditionViaTokenArgs.from_json(json_obj)
    assert args.edition == 42
