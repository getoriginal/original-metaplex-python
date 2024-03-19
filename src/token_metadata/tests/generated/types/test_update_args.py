from solders.pubkey import Pubkey

from src.token_metadata.generated.types import Payload, authorization_data, data
from src.token_metadata.generated.types.collection_details_toggle import (
    None_ as CollectionDetailsToggleNone,
)
from src.token_metadata.generated.types.collection_toggle import (
    None_ as CollectionToggleNone,
)
from src.token_metadata.generated.types.rule_set_toggle import None_ as RuleSetNone
from src.token_metadata.generated.types.token_standard import NonFungible
from src.token_metadata.generated.types.update_args import (
    V1,
    AsAuthorityItemDelegateV2,
    AsCollectionDelegateV2,
    AsCollectionItemDelegateV2,
    AsDataDelegateV2,
    AsDataItemDelegateV2,
    AsProgrammableConfigDelegateV2,
    AsProgrammableConfigItemDelegateV2,
    from_json,
)
from src.token_metadata.generated.types.uses_toggle import None_ as UsesNone

auth_data_example = authorization_data.AuthorizationData(payload=Payload(map=True))
collection_example = CollectionToggleNone()
collection_details_example = CollectionDetailsToggleNone()
uses_example = UsesNone()
rule_set_example = RuleSetNone()
token_standard_example = NonFungible()
data_example = data.Data(
    name="Example",
    symbol="EX",
    uri="http://example.com",
    seller_fee_basis_points=1000,
    creators=[],
)


def test_update_args_v1_to_json():
    new_update_authority = Pubkey.new_unique()
    v1 = V1(
        value={
            "new_update_authority": new_update_authority,
            "data": data_example,
            "primary_sale_happened": True,
            "is_mutable": True,
            "collection": collection_example,
            "collection_details": collection_details_example,
            "uses": uses_example,
            "rule_set": rule_set_example,
            "authorization_data": auth_data_example,
        }
    )
    json_obj = v1.to_json()
    assert json_obj == {
        "kind": "V1",
        "value": {
            "new_update_authority": str(new_update_authority),
            "data": data_example.to_json(),
            "primary_sale_happened": True,
            "is_mutable": True,
            "collection": collection_example.to_json(),
            "collection_details": collection_details_example.to_json(),
            "uses": uses_example.to_json(),
            "rule_set": rule_set_example.to_json(),
            "authorization_data": auth_data_example.to_json(),
        },
    }


def test_update_args_v1_from_json():
    new_update_authority_str = str(Pubkey.new_unique())
    json_obj = {
        "kind": "V1",
        "value": {
            "new_update_authority": new_update_authority_str,
            "data": data_example.to_json(),
            "primary_sale_happened": True,
            "is_mutable": True,
            "collection": collection_example.to_json(),
            "collection_details": collection_details_example.to_json(),
            "uses": uses_example.to_json(),
            "rule_set": rule_set_example.to_json(),
            "authorization_data": auth_data_example.to_json(),
        },
    }
    kind = from_json(json_obj)
    assert (
        isinstance(kind, V1)
        and str(kind.value["new_update_authority"]) == new_update_authority_str
    )


def test_as_authority_item_delegate_v2_to_json():
    new_update_authority = Pubkey.new_unique()
    as_authority_item_delegate_v2 = AsAuthorityItemDelegateV2(
        value={
            "new_update_authority": new_update_authority,
            "primary_sale_happened": True,
            "is_mutable": True,
            "token_standard": token_standard_example,
            "authorization_data": auth_data_example,
        }
    )
    json_obj = as_authority_item_delegate_v2.to_json()
    assert json_obj == {
        "kind": "AsAuthorityItemDelegateV2",
        "value": {
            "new_update_authority": str(new_update_authority),
            "primary_sale_happened": True,
            "is_mutable": True,
            "token_standard": token_standard_example.to_json(),
            "authorization_data": auth_data_example.to_json(),
        },
    }


def test_as_authority_item_delegate_v2_from_json():
    new_update_authority_str = str(Pubkey.new_unique())
    json_obj = {
        "kind": "AsAuthorityItemDelegateV2",
        "value": {
            "new_update_authority": new_update_authority_str,
            "primary_sale_happened": True,
            "is_mutable": True,
            "token_standard": token_standard_example.to_json(),
            "authorization_data": auth_data_example.to_json(),
        },
    }
    kind = from_json(json_obj)
    assert (
        isinstance(kind, AsAuthorityItemDelegateV2)
        and str(kind.value["new_update_authority"]) == new_update_authority_str
    )


def test_as_collection_delegate_v2_to_json():
    as_collection_delegate_v2 = AsCollectionDelegateV2(
        value={
            "collection": collection_example,
            "authorization_data": auth_data_example,
        }
    )
    json_obj = as_collection_delegate_v2.to_json()
    assert json_obj == {
        "kind": "AsCollectionDelegateV2",
        "value": {
            "collection": collection_example.to_json(),
            "authorization_data": auth_data_example.to_json(),
        },
    }


def test_as_collection_delegate_v2_from_json():
    json_obj = {
        "kind": "AsCollectionDelegateV2",
        "value": {
            "collection": collection_example.to_json(),
            "authorization_data": auth_data_example.to_json(),
        },
    }
    kind = from_json(json_obj)
    assert isinstance(kind, AsCollectionDelegateV2)


def test_as_data_delegate_v2_to_json():
    as_data_delegate_v2 = AsDataDelegateV2(
        value={"data": data_example, "authorization_data": auth_data_example}
    )
    json_obj = as_data_delegate_v2.to_json()
    assert json_obj == {
        "kind": "AsDataDelegateV2",
        "value": {
            "data": data_example.to_json(),
            "authorization_data": auth_data_example.to_json(),
        },
    }


def test_as_data_delegate_v2_from_json():
    json_obj = {
        "kind": "AsDataDelegateV2",
        "value": {
            "data": data_example.to_json(),
            "authorization_data": auth_data_example.to_json(),
        },
    }
    kind = from_json(json_obj)
    assert isinstance(kind, AsDataDelegateV2)


def test_as_programmable_config_delegate_v2_to_json():
    as_programmable_config_delegate_v2 = AsProgrammableConfigDelegateV2(
        value={"rule_set": rule_set_example, "authorization_data": auth_data_example}
    )
    json_obj = as_programmable_config_delegate_v2.to_json()
    assert json_obj == {
        "kind": "AsProgrammableConfigDelegateV2",
        "value": {
            "rule_set": rule_set_example.to_json(),
            "authorization_data": auth_data_example.to_json(),
        },
    }


def test_as_programmable_config_delegate_v2_from_json():
    json_obj = {
        "kind": "AsProgrammableConfigDelegateV2",
        "value": {
            "rule_set": rule_set_example.to_json(),
            "authorization_data": auth_data_example.to_json(),
        },
    }
    kind = from_json(json_obj)
    assert isinstance(kind, AsProgrammableConfigDelegateV2)


def test_as_data_item_delegate_v2_to_json():
    as_data_item_delegate_v2 = AsDataItemDelegateV2(
        value={"data": data_example, "authorization_data": auth_data_example}
    )
    json_obj = as_data_item_delegate_v2.to_json()
    assert json_obj == {
        "kind": "AsDataItemDelegateV2",
        "value": {
            "data": data_example.to_json(),
            "authorization_data": auth_data_example.to_json(),
        },
    }


def test_as_data_item_delegate_v2_from_json():
    json_obj = {
        "kind": "AsDataItemDelegateV2",
        "value": {
            "data": data_example.to_json(),
            "authorization_data": auth_data_example.to_json(),
        },
    }
    kind = from_json(json_obj)
    assert isinstance(kind, AsDataItemDelegateV2)


def test_as_collection_item_delegate_v2_to_json():
    as_collection_item_delegate_v2 = AsCollectionItemDelegateV2(
        value={
            "collection": collection_example,
            "authorization_data": auth_data_example,
        }
    )
    json_obj = as_collection_item_delegate_v2.to_json()
    assert json_obj == {
        "kind": "AsCollectionItemDelegateV2",
        "value": {
            "collection": collection_example.to_json(),
            "authorization_data": auth_data_example.to_json(),
        },
    }


def test_as_collection_item_delegate_v2_from_json():
    json_obj = {
        "kind": "AsCollectionItemDelegateV2",
        "value": {
            "collection": collection_example.to_json(),
            "authorization_data": auth_data_example.to_json(),
        },
    }
    kind = from_json(json_obj)
    assert isinstance(kind, AsCollectionItemDelegateV2)


def test_as_programmable_config_item_delegate_v2_to_json():
    as_programmable_config_item_delegate_v2 = AsProgrammableConfigItemDelegateV2(
        value={"rule_set": rule_set_example, "authorization_data": auth_data_example}
    )
    json_obj = as_programmable_config_item_delegate_v2.to_json()
    assert json_obj == {
        "kind": "AsProgrammableConfigItemDelegateV2",
        "value": {
            "rule_set": rule_set_example.to_json(),
            "authorization_data": auth_data_example.to_json(),
        },
    }


def test_as_programmable_config_item_delegate_v2_from_json():
    json_obj = {
        "kind": "AsProgrammableConfigItemDelegateV2",
        "value": {
            "rule_set": rule_set_example.to_json(),
            "authorization_data": auth_data_example.to_json(),
        },
    }
    kind = from_json(json_obj)
    assert isinstance(kind, AsProgrammableConfigItemDelegateV2)
