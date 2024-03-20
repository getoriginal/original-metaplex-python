from original_metaplex_python.token_metadata.generated.types.collection_details_toggle import (
    Clear,
    None_,
    Set,
    from_decoded,
    from_json,
)


def test_from_decoded_none():
    decoded = {"None": {}}
    instance = from_decoded(decoded)
    assert isinstance(instance, None_)


def test_from_decoded_clear():
    decoded = {"Clear": {}}
    instance = from_decoded(decoded)
    assert isinstance(instance, Clear)


def test_from_decoded_set():
    decoded = {"Set": {"item_0": {"V1": {"size": 10}}}}
    instance = from_decoded(decoded)
    assert isinstance(instance, Set)
    assert instance.value[0].value == {"size": 10}


def test_from_json_none():
    json_data = {"kind": "None"}
    instance = from_json(json_data)
    assert isinstance(instance, None_)


def test_from_json_clear():
    json_data = {"kind": "Clear"}
    instance = from_json(json_data)
    assert isinstance(instance, Clear)


def test_from_json_set():
    json_data = {
        "kind": "Set",
        "value": [{"kind": "V1", "value": {"size": 10}}],
    }
    instance = from_json(json_data)
    assert isinstance(instance, Set)
    assert instance.value[0].value == {"size": 10}
