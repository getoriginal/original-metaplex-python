from dataclasses import asdict

from construct import Container

from original_metaplex_python.token_metadata.generated.types import (
    ApproveUseAuthorityArgs,
)


def test_approve_use_authority_args_to_encodable():
    args = ApproveUseAuthorityArgs(number_of_uses=5)
    encodable = args.to_encodable()
    assert encodable == {"number_of_uses": 5}


def test_approve_use_authority_args_from_decoded():
    decoded = Container(number_of_uses=5)
    args = ApproveUseAuthorityArgs.from_decoded(decoded)

    assert args.number_of_uses == 5


def test_approve_use_authority_args_to_json():
    args = ApproveUseAuthorityArgs(number_of_uses=5)
    json_obj = args.to_json()
    assert json_obj == {"number_of_uses": 5}


def test_approve_use_authority_args_from_json():
    json_obj = {"number_of_uses": 5}
    args = ApproveUseAuthorityArgs.from_json(json_obj)
    assert args.number_of_uses == 5


def test_approve_use_authority_args_dataclass():
    args = ApproveUseAuthorityArgs(number_of_uses=5)
    assert asdict(args) == {"number_of_uses": 5}
