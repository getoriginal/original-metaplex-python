from dataclasses import asdict

from construct import Container

from original_metaplex_python.token_metadata.generated.types.transfer_out_of_escrow_args import (
    TransferOutOfEscrowArgs,
)


def test_transfer_out_of_escrow_args_to_encodable():
    args = TransferOutOfEscrowArgs(amount=100)
    encodable = args.to_encodable()
    assert encodable == {"amount": 100}


def test_transfer_out_of_escrow_args_from_decoded():
    decoded = Container(amount=100)
    args = TransferOutOfEscrowArgs.from_decoded(decoded)
    assert isinstance(args, TransferOutOfEscrowArgs) and args.amount == 100


def test_transfer_out_of_escrow_args_to_json():
    args = TransferOutOfEscrowArgs(amount=100)
    json_obj = args.to_json()
    assert json_obj == {"amount": 100}


def test_transfer_out_of_escrow_args_from_json():
    json_obj = {"amount": 100}
    args = TransferOutOfEscrowArgs.from_json(json_obj)
    assert isinstance(args, TransferOutOfEscrowArgs) and args.amount == 100


def test_transfer_out_of_escrow_args_dataclass():
    args = TransferOutOfEscrowArgs(amount=100)
    assert asdict(args) == {"amount": 100}
