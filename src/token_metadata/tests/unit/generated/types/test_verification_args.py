from src.token_metadata.generated.types.verification_args import (
    CollectionV1,
    CreatorV1,
    from_decoded,
    from_json,
)


def test_creator_v1_to_encodable():
    creator_v1 = CreatorV1()
    encodable = creator_v1.to_encodable()
    assert encodable == {"CreatorV1": {}}


def test_creator_v1_to_json():
    creator_v1 = CreatorV1()
    json_obj = creator_v1.to_json()
    assert json_obj == {"kind": "CreatorV1"}


def test_collection_v1_to_encodable():
    collection_v1 = CollectionV1()
    encodable = collection_v1.to_encodable()
    assert encodable == {"CollectionV1": {}}


def test_collection_v1_to_json():
    collection_v1 = CollectionV1()
    json_obj = collection_v1.to_json()
    assert json_obj == {"kind": "CollectionV1"}


def test_verification_args_from_decoded():
    decoded_creator = {"CreatorV1": {}}
    result_creator = from_decoded(decoded_creator)
    assert isinstance(result_creator, CreatorV1)

    decoded_collection = {"CollectionV1": {}}
    result_collection = from_decoded(decoded_collection)
    assert isinstance(result_collection, CollectionV1)


def test_verification_args_from_json():
    json_creator = {"kind": "CreatorV1"}
    result_creator = from_json(json_creator)
    assert isinstance(result_creator, CreatorV1)

    json_collection = {"kind": "CollectionV1"}
    result_collection = from_json(json_collection)
    assert isinstance(result_collection, CollectionV1)
