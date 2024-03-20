from solders.pubkey import Pubkey

from original_metaplex_python.token_metadata.generated.types.escrow_authority import (
    Creator,
    TokenOwner,
    from_decoded,
    from_json,
)


def test_token_owner_to_json():
    token_owner = TokenOwner()
    json_obj = token_owner.to_json()
    assert json_obj == {"kind": "TokenOwner"}


def test_token_owner_to_encodable():
    token_owner = TokenOwner()
    encodable = token_owner.to_encodable()
    assert encodable == {"TokenOwner": {}}


def test_creator_to_json():
    creator = Creator(value=(Pubkey.new_unique(),))
    json_obj = creator.to_json()
    assert json_obj == {"kind": "Creator", "value": (str(creator.value[0]),)}


def test_creator_to_encodable():
    creator = Creator(value=(Pubkey.new_unique(),))
    encodable = creator.to_encodable()
    assert encodable == {"Creator": {"item_0": creator.value[0]}}


def test_from_decoded_token_owner():
    decoded = {"TokenOwner": {}}
    obj = from_decoded(decoded)
    assert isinstance(obj, TokenOwner)


def test_from_decoded_creator():
    pubkey = Pubkey.new_unique()
    decoded = {"Creator": {"item_0": pubkey}}
    obj = from_decoded(decoded)
    assert isinstance(obj, Creator)
    assert obj.value[0] == pubkey


def test_from_json_token_owner():
    json_obj = {"kind": "TokenOwner"}
    obj = from_json(json_obj)
    assert isinstance(obj, TokenOwner)


def test_from_json_creator():
    pubkey = Pubkey.new_unique()
    json_obj = {"kind": "Creator", "value": (str(pubkey),)}
    obj = from_json(json_obj)
    assert isinstance(obj, Creator)
    assert obj.value[0] == pubkey
