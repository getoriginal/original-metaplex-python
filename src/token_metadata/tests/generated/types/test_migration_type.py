from src.token_metadata.generated.types import migration_type
from src.token_metadata.generated.types.migration_type import (
    CollectionV1,
    ProgrammableV1,
)


def test_migration_type_to_encodable_collection_v1():
    instance = CollectionV1()
    encodable = instance.to_encodable()
    assert encodable == {"CollectionV1": {}}


def test_migration_type_from_json_collection_v1():
    json_obj = {"kind": "CollectionV1"}
    instance = migration_type.from_json(json_obj)
    assert isinstance(instance, CollectionV1)


def test_migration_type_to_json_collection_v1():
    instance = CollectionV1()
    json_obj = instance.to_json()
    assert json_obj == {"kind": "CollectionV1"}


def test_migration_type_to_encodable_programmable_v1():
    instance = ProgrammableV1()
    encodable = instance.to_encodable()
    assert encodable == {"ProgrammableV1": {}}


def test_migration_type_from_json_programmable_v1():
    json_obj = {"kind": "ProgrammableV1"}
    instance = migration_type.from_json(json_obj)
    assert isinstance(instance, ProgrammableV1)


def test_migration_type_to_json_programmable_v1():
    instance = ProgrammableV1()
    json_obj = instance.to_json()
    assert json_obj == {"kind": "ProgrammableV1"}
