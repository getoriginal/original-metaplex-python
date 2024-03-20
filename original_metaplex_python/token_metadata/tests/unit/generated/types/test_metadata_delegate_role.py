from original_metaplex_python.token_metadata.generated.types import (
    metadata_delegate_role,
)
from original_metaplex_python.token_metadata.generated.types.metadata_delegate_role import (
    AuthorityItem,
    Collection,
    CollectionItem,
    Data,
    DataItem,
    ProgrammableConfig,
    ProgrammableConfigItem,
    Use,
)


def test_metadata_delegate_role_to_encodable():
    authority_item_instance = AuthorityItem()
    encodable = authority_item_instance.to_encodable()

    assert encodable == {"AuthorityItem": {}}


def test_metadata_delegate_role_from_json():
    json_obj = {"kind": "AuthorityItem"}
    instance = metadata_delegate_role.from_json(json_obj)

    assert isinstance(instance, AuthorityItem)


def test_metadata_delegate_role_to_json():
    authority_item_instance = AuthorityItem()
    json_obj = authority_item_instance.to_json()

    assert json_obj == {"kind": "AuthorityItem"}


def test_collection_to_encodable():
    collection_instance = Collection()
    encodable = collection_instance.to_encodable()

    assert encodable == {"Collection": {}}


def test_use_to_encodable():
    use_instance = Use()
    encodable = use_instance.to_encodable()

    assert encodable == {"Use": {}}


def test_data_to_encodable():
    data_instance = Data()
    encodable = data_instance.to_encodable()

    assert encodable == {"Data": {}}


def test_programmable_config_to_encodable():
    programmable_config_instance = ProgrammableConfig()
    encodable = programmable_config_instance.to_encodable()

    assert encodable == {"ProgrammableConfig": {}}


def test_data_item_to_encodable():
    data_item_instance = DataItem()
    encodable = data_item_instance.to_encodable()

    assert encodable == {"DataItem": {}}


def test_collection_item_to_encodable():
    collection_item_instance = CollectionItem()
    encodable = collection_item_instance.to_encodable()

    assert encodable == {"CollectionItem": {}}


def test_programmable_config_item_to_encodable():
    programmable_config_item_instance = ProgrammableConfigItem()
    encodable = programmable_config_item_instance.to_encodable()

    assert encodable == {"ProgrammableConfigItem": {}}
