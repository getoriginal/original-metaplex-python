from solders.pubkey import Pubkey

from original_metaplex_python.token_metadata.generated.types.authorization_data import (
    AuthorizationData,
)
from original_metaplex_python.token_metadata.generated.types.delegate_args import (
    AuthorityItemV1,
    CollectionItemV1,
    CollectionV1,
    DataItemV1,
    LockedTransferV1,
    ProgrammableConfigItemV1,
    ProgrammableConfigV1,
    SaleV1,
    StandardV1,
    TransferV1,
)
from original_metaplex_python.token_metadata.generated.types.payload import Payload


def test_collection_v1_to_json():
    authorization_data_instance = AuthorizationData(payload=Payload(map=True))
    collection_v1_instance = CollectionV1(
        value={"authorization_data": authorization_data_instance}
    )
    json_data = collection_v1_instance.to_json()
    assert json_data["kind"] == "CollectionV1"
    assert json_data["value"]["authorization_data"] is not None


def test_sale_v1_to_json():
    authorization_data_instance = AuthorizationData(payload=Payload(map=True))
    sale_v1_instance = SaleV1(
        value={"amount": 100, "authorization_data": authorization_data_instance}
    )
    json_data = sale_v1_instance.to_json()
    assert json_data["kind"] == "SaleV1"
    assert json_data["value"]["amount"] == 100
    assert json_data["value"]["authorization_data"] is not None


def test_transfer_v1_to_json():
    authorization_data_instance = AuthorizationData(payload=Payload(map=True))
    transfer_v1_instance = TransferV1(
        value={"amount": 200, "authorization_data": authorization_data_instance}
    )
    json_data = transfer_v1_instance.to_json()
    assert json_data["kind"] == "TransferV1"
    assert json_data["value"]["amount"] == 200
    assert json_data["value"]["authorization_data"] is not None


def test_standard_v1_to_json():
    standard_v1_instance = StandardV1(value={"amount": 300})
    json_data = standard_v1_instance.to_json()
    assert json_data["kind"] == "StandardV1"
    assert json_data["value"]["amount"] == 300


def test_locked_transfer_v1_to_json():
    authorization_data_instance = AuthorizationData(payload=Payload(map=True))
    locked_address = Pubkey.new_unique()
    locked_transfer_v1_instance = LockedTransferV1(
        value={
            "amount": 400,
            "locked_address": locked_address,
            "authorization_data": authorization_data_instance,
        }
    )
    json_data = locked_transfer_v1_instance.to_json()
    assert json_data["kind"] == "LockedTransferV1"
    assert json_data["value"]["amount"] == 400
    assert str(json_data["value"]["locked_address"]) == str(locked_address)
    assert json_data["value"]["authorization_data"] is not None


def test_programmable_config_v1_to_json():
    authorization_data_instance = AuthorizationData(payload=Payload(map=True))
    programmable_config_v1_instance = ProgrammableConfigV1(
        value={"authorization_data": authorization_data_instance}
    )
    json_data = programmable_config_v1_instance.to_json()
    assert json_data["kind"] == "ProgrammableConfigV1"
    assert json_data["value"]["authorization_data"] is not None


def test_authority_item_v1_to_json():
    authorization_data_instance = AuthorizationData(payload=Payload(map=True))
    authority_item_v1_instance = AuthorityItemV1(
        value={"authorization_data": authorization_data_instance}
    )
    json_data = authority_item_v1_instance.to_json()
    assert json_data["kind"] == "AuthorityItemV1"
    assert json_data["value"]["authorization_data"] is not None


def test_data_item_v1_to_json():
    authorization_data_instance = AuthorizationData(payload=Payload(map=True))
    data_item_v1_instance = DataItemV1(
        value={"authorization_data": authorization_data_instance}
    )
    json_data = data_item_v1_instance.to_json()
    assert json_data["kind"] == "DataItemV1"
    assert json_data["value"]["authorization_data"] is not None


def test_collection_item_v1_to_json():
    authorization_data_instance = AuthorizationData(payload=Payload(map=True))
    collection_item_v1_instance = CollectionItemV1(
        value={"authorization_data": authorization_data_instance}
    )
    json_data = collection_item_v1_instance.to_json()
    assert json_data["kind"] == "CollectionItemV1"
    assert json_data["value"]["authorization_data"] is not None


def test_programmable_config_item_v1_to_json():
    authorization_data_instance = AuthorizationData(payload=Payload(map=True))
    programmable_config_item_v1_instance = ProgrammableConfigItemV1(
        value={"authorization_data": authorization_data_instance}
    )
    json_data = programmable_config_item_v1_instance.to_json()
    assert json_data["kind"] == "ProgrammableConfigItemV1"
    assert json_data["value"]["authorization_data"] is not None
