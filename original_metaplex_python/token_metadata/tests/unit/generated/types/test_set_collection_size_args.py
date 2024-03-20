from dataclasses import asdict

from construct import Container

from original_metaplex_python.token_metadata.generated.types.set_collection_size_args import (
    SetCollectionSizeArgs,
)


def test_set_collection_size_args_to_encodable():
    args = SetCollectionSizeArgs(size=500)
    encodable = args.to_encodable()
    assert encodable == {"size": 500}


def test_set_collection_size_args_from_decoded():
    decoded = Container(size=500)
    args = SetCollectionSizeArgs.from_decoded(decoded)
    assert args.size == 500


def test_set_collection_size_args_to_json():
    args = SetCollectionSizeArgs(size=500)
    json_obj = args.to_json()
    assert json_obj == {"size": 500}


def test_set_collection_size_args_from_json():
    json_obj = {"size": 500}
    args = SetCollectionSizeArgs.from_json(json_obj)
    assert args.size == 500


def test_set_collection_size_args_dataclass():
    args = SetCollectionSizeArgs(size=500)
    assert asdict(args) == {"size": 500}
