from src.token_metadata.generated.types.authority_type import (
    Holder,
    Metadata,
    MetadataDelegate,
    None_,
    TokenDelegate,
    from_decoded,
    from_json,
)


def test_none_to_json():
    none = None_()
    json_obj = none.to_json()
    assert json_obj == {"kind": "None"}


def test_metadata_to_json():
    metadata = Metadata()
    json_obj = metadata.to_json()
    assert json_obj == {"kind": "Metadata"}


def test_holder_to_json():
    holder = Holder()
    json_obj = holder.to_json()
    assert json_obj == {"kind": "Holder"}


def test_metadata_delegate_to_json():
    metadata_delegate = MetadataDelegate()
    json_obj = metadata_delegate.to_json()
    assert json_obj == {"kind": "MetadataDelegate"}


def test_token_delegate_to_json():
    token_delegate = TokenDelegate()
    json_obj = token_delegate.to_json()
    assert json_obj == {"kind": "TokenDelegate"}


def test_from_decoded_none():
    obj = {"None": {}}
    result = from_decoded(obj)
    assert isinstance(result, None_)


def test_from_decoded_metadata():
    obj = {"Metadata": {}}
    result = from_decoded(obj)
    assert isinstance(result, Metadata)


def test_from_decoded_holder():
    obj = {"Holder": {}}
    result = from_decoded(obj)
    assert isinstance(result, Holder)


def test_from_decoded_metadata_delegate():
    obj = {"MetadataDelegate": {}}
    result = from_decoded(obj)
    assert isinstance(result, MetadataDelegate)


def test_from_decoded_token_delegate():
    obj = {"TokenDelegate": {}}
    result = from_decoded(obj)
    assert isinstance(result, TokenDelegate)


def test_from_json_none():
    json_obj = {"kind": "None"}
    result = from_json(json_obj)
    assert isinstance(result, None_)


def test_from_json_metadata():
    json_obj = {"kind": "Metadata"}
    result = from_json(json_obj)
    assert isinstance(result, Metadata)


def test_from_json_holder():
    json_obj = {"kind": "Holder"}
    result = from_json(json_obj)
    assert isinstance(result, Holder)


def test_from_json_metadata_delegate():
    json_obj = {"kind": "MetadataDelegate"}
    result = from_json(json_obj)
    assert isinstance(result, MetadataDelegate)


def test_from_json_token_delegate():
    json_obj = {"kind": "TokenDelegate"}
    result = from_json(json_obj)
    assert isinstance(result, TokenDelegate)
